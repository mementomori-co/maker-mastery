r"""test_audit_checks.py - audit_3mf.py checks C1-C6 and C8-C16 on synthetic 3MF files.

Run: .venv\Scripts\python.exe -B -m unittest discover -s tools\tests -p "test_audit*.py" -v
No Bambu Studio, Blender or network needed (fixtures_3mf isolates the config).
"""
import io
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import fixtures_3mf as fx  # noqa: E402
    import audit_3mf  # noqa: E402
except ImportError as _e:  # pragma: no cover - packages from requirements.txt not installed yet
    raise unittest.SkipTest(f"a package from requirements.txt is missing ({_e}); run tools\\setup.ps1 and answer y")

F, P = fx.find, fx.project


class TestGroupingAndArea(unittest.TestCase):
    def two_fil(self, **over):
        return P(filament_settings_id=["Bambu PLA Basic @BBL H2C"] * 2, filament_ids=["GFA00"] * 2,
                 filament_colour=["#000000FF", "#FFFFFFFF"], filament_type=["PLA", "PLA"], filament_map=["2", "2"],
                 textured_plate_temp=["55", "55"], temperature_vitrification=["70", "70"], **over)

    def test_c1_auto_mode_with_two_filaments_warns(self):
        p = self.two_fil(filament_map_mode="Auto For Flush")
        path = fx.build(proj=p, plates=fx.default_plates(mode="Auto For Flush", maps="2 2"),
                        plate_json={1: {"filament_ids": [0, 1], "bbox_objects": []}})
        _, r = fx.run(path, geometry=False)
        self.assertEqual(fx.levels(F(r, "C1")), {"WARN"})
        self.assertIn("LEFT extruder", F(r, "C1")[0]["msg"])

    def test_c1_manual_ok(self):
        path = fx.build(proj=self.two_fil(), plates=fx.default_plates(maps="2 2"),
                        plate_json={1: {"filament_ids": [0, 1], "bbox_objects": []}})
        _, r = fx.run(path, geometry=False)
        self.assertEqual(fx.levels(F(r, "C1")), {"OK"})

    def test_c2_slice_info_disagrees_fails(self):
        p = P()
        path = fx.build(proj=p, gcodes={1: fx.gcode(p)}, slice_info=fx.slice_info_xml(maps="1"))
        _, r = fx.run(path, geometry=False)
        c2 = F(r, "C2")
        self.assertIn("FAIL", fx.levels(c2))
        self.assertIn("slice_info.config filament_maps = '1'", next(f["msg"] for f in c2 if f["level"] == "FAIL"))
        # the effective (slice_info) map is what C7 L6 judges: RIGHT row vs map 1 -> FAIL
        self.assertEqual(fx.levels(F(r, "C7", "L6")), {"FAIL"})

    def test_c2_slice_info_agrees_ok(self):
        p = P()
        _, r = fx.run(fx.build(proj=p, gcodes={1: fx.gcode(p)}, slice_info=fx.slice_info_xml()), geometry=False)
        self.assertEqual(fx.levels(F(r, "C2")), {"OK"})

    def test_c3_zero_bridge_length_warns(self):
        _, r = fx.run(fx.build(proj=P(max_bridge_length="0")), geometry=False)
        self.assertEqual(fx.levels(F(r, "C3")), {"WARN"})
        _, r = fx.run(fx.build(), geometry=False)
        self.assertEqual(fx.levels(F(r, "C3")), {"OK"})

    def test_c5_object_outside_right_area_fails(self):
        pj = {1: {"filament_ids": [0], "bbox_objects": [{"name": "test_block", "bbox": [10.0, 50.0, 40.0, 80.0]}]}}
        _, r = fx.run(fx.build(plate_json=pj), geometry=False)   # maps "2" -> right area 25..330
        self.assertEqual(fx.levels(F(r, "C5")), {"FAIL"})
        pj[1]["bbox_objects"][0]["bbox"] = [100.0, 50.0, 140.0, 80.0]
        _, r = fx.run(fx.build(plate_json=pj), geometry=False)
        self.assertEqual(fx.levels(F(r, "C5")), {"OK"})

    def test_c6_reports_tower(self):
        _, r = fx.run(fx.build(), geometry=False)
        self.assertIn("clearance not computed here", F(r, "C6")[0]["msg"])


class TestBed(unittest.TestCase):
    def test_c9_zero_bed_temp_fails(self):
        _, r = fx.run(fx.build(proj=P(textured_plate_temp=["0"])), geometry=False)
        self.assertEqual(fx.levels(F(r, "C9")), {"FAIL"})
        self.assertIn("does not support filament", F(r, "C9")[0]["msg"])

    def test_c9_outside_plate_range_warns(self):
        _, r = fx.run(fx.build(proj=P(textured_plate_temp=["80"], temperature_vitrification=["90"])), geometry=False)
        self.assertEqual(fx.levels(F(r, "C9")), {"WARN"})
        self.assertIn("outside plate table 45-65", F(r, "C9")[0]["msg"])

    def test_c9_h2_cooling_unsliced_warns_sliced_ok(self):
        p = P(textured_plate_temp=["60"], temperature_vitrification=["55"])
        _, r = fx.run(fx.build(proj=p), geometry=False)
        msgs = [f["msg"] for f in F(r, "C9") if f["level"] == "WARN"]
        self.assertTrue(any("not verified: slice and re-audit" in m for m in msgs), msgs)
        g = fx.gcode(p, start=["M145 P0", "M106 P3 S255"])
        _, r = fx.run(fx.build(proj=p, gcodes={1: g}), geometry=False)
        self.assertTrue(any(f["level"] == "OK" and "M145 P0 and M106 P3 found" in f["msg"] for f in F(r, "C9")), F(r, "C9"))
        g2 = fx.gcode(p, start=["M145 P0"])   # exhaust missing
        _, r = fx.run(fx.build(proj=p, gcodes={1: g2}), geometry=False)
        self.assertTrue(any("not found in plate G-code start section" in f["msg"] for f in F(r, "C9")))

    def test_c9_other_printer_door_rule_warns(self):
        p = P(printer_settings_id="Bambu Lab P1S 0.4 nozzle", textured_plate_temp=["60"], temperature_vitrification=["55"])
        _, r = fx.run(fx.build(proj=p), geometry=False)
        self.assertTrue(any(f["level"] == "WARN" and "open the front door" in f["msg"] for f in F(r, "C9")))

    def test_c9_unknown_bed_warns(self):
        _, r = fx.run(fx.build(proj=P(curr_bed_type="Mystery Plate")), geometry=False)
        self.assertEqual(fx.levels(F(r, "C9")), {"WARN"})


class TestInfill(unittest.TestCase):
    def test_project_100_grid_fails_concentric_ok(self):
        _, r = fx.run(fx.build(proj=P(sparse_infill_density="100%")), geometry=False)
        self.assertEqual(fx.levels(F(r, "C10")), {"FAIL"})
        self.assertIn("CLI_INVALID_VALUES_IN_3MF", F(r, "C10")[0]["msg"])
        _, r = fx.run(fx.build(proj=P(sparse_infill_density="100%", sparse_infill_pattern="concentric")), geometry=False)
        self.assertEqual(fx.levels(F(r, "C10")), {"OK"})

    def test_object_and_part_override(self):
        objs = fx.default_objects(meta={"sparse_infill_density": "100%", "sparse_infill_pattern": "gyroid"})
        _, r = fx.run(fx.build(objects=objs), geometry=False)
        self.assertEqual(fx.levels(F(r, "C10")), {"FAIL"})
        self.assertIn("slices it with holes", F(r, "C10")[0]["msg"])
        objs = fx.default_objects()
        objs[0]["parts"][0]["meta"] = {"sparse_infill_density": "100"}
        _, r = fx.run(fx.build(objects=objs), geometry=False)
        self.assertEqual(fx.levels(F(r, "C10")), {"FAIL"})
        self.assertTrue(F(r, "C10")[0]["msg"].startswith("part 1"))

    def test_height_range_resolved_and_unresolved(self):
        rng = ('<objects><object id="1"><range min_z="2" max_z="5"><option opt_key="sparse_infill_density">100%</option>'
               '</range></object></objects>')
        _, r = fx.run(fx.build(ranges_xml=rng), geometry=False)
        self.assertEqual(fx.levels(F(r, "C10")), {"FAIL"})
        self.assertIn("height range 2-5 mm", F(r, "C10")[0]["msg"])
        rng5 = rng.replace('object id="1"', 'object id="5"')
        _, r = fx.run(fx.build(ranges_xml=rng5), geometry=False)
        self.assertIn("not resolved", F(r, "C10")[0]["msg"])
        self.assertEqual(F(r, "C10")[0]["level"], "WARN")


class TestSource(unittest.TestCase):
    def test_c11_skipped_without_source(self):
        _, r = fx.run(fx.build(), geometry=False)
        self.assertEqual(fx.levels(F(r, "C11")), {"OK"})
        self.assertIn("skipped", F(r, "C11")[0]["msg"])

    def test_c11_swap_fails_then_approved(self):
        src = fx.build(name="design_intent")
        p = P(filament_settings_id=["Generic PETG @BBL H2C"], filament_type=["PETG"], filament_ids=["GFG99"], textured_plate_temp=["70"])
        out = fx.build(proj=p)
        _, r = fx.run(out, "--source", src, geometry=False)
        self.assertEqual(fx.levels(F(r, "C11")), {"FAIL"})
        self.assertEqual(r["source_assignment"]["fail"], 1)
        uuid = fx.default_objects()[0]["parts"][0]["uuid"]
        _, r = fx.run(out, "--source", src, "--approve-swap", f"{uuid}=1:maker/2026-01-10", geometry=False)
        self.assertEqual(fx.levels(F(r, "C11")), {"OK"})
        self.assertEqual(r["source_assignment"]["approved"], 1)

    def test_c11_same_line_ok_and_missing_part_warns(self):
        src_objs = fx.default_objects() + [{"id": "2", "name": "lid", "meta": {"extruder": "1"},
                                            "parts": [{"id": "2", "subtype": "normal_part", "name": "lid", "meta": {}, "uuid": "u-lid"}]}]
        src = fx.build(objects=src_objs, name="design_two_parts")
        _, r = fx.run(fx.build(), "--source", src, geometry=False)
        c11 = F(r, "C11")
        self.assertTrue(any(f["level"] == "OK" and "= source" in f["msg"] for f in c11))
        self.assertTrue(any(f["level"] == "WARN" and "part not found" in f["msg"] for f in c11))
        self.assertEqual(r["source_assignment"]["missing"], 1)

    def test_c11_malformed_approval_exits_64(self):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as cm:
            audit_3mf.main(["audit_3mf.py", fx.build(), "--source", fx.build(), "--approve-swap", "nonsense",
                            "--load-note", fx.load_note(), "--today", fx.TODAY, "--no-geometry"])
        self.assertEqual(cm.exception.code, 64)

    def test_c11_unreadable_source_fails(self):
        bad = os.path.join(fx.WORK, "not_a_zip.3mf")
        with open(bad, "w", encoding="utf-8") as f:
            f.write("plain text")
        _, r = fx.run(fx.build(), "--source", bad, geometry=False)
        self.assertEqual(fx.levels(F(r, "C11")), {"FAIL"})


class TestFlatTops(unittest.TestCase):
    def test_large_flat_top_warns_small_ok(self):
        _, r = fx.run(fx.build(meshes={"1": fx.box(0, 0, 0, 30, 30, 10)}))
        c12 = F(r, "C12")
        self.assertEqual(fx.levels(c12), {"WARN"})
        self.assertIn("flat up-facing area 900.0 mm2", c12[0]["msg"])
        geo = r["objects_geometry"][0]
        self.assertAlmostEqual(geo["top_z"], 10.0)
        self.assertAlmostEqual(geo["top_flat_mm2"], 900.0)
        _, r = fx.run(fx.build())   # 10 x 10 top = 100 mm2
        self.assertEqual(fx.levels(F(r, "C12")), {"OK"})

    def test_no_geometry_skips(self):
        _, r = fx.run(fx.build(meshes={"1": fx.box(0, 0, 0, 30, 30, 10)}), geometry=False)
        self.assertEqual(fx.levels(F(r, "C12")), {"OK"})
        self.assertIn("skipped (--no-geometry)", F(r, "C12")[0]["msg"])

    def test_topmost_ironing_with_lower_flat_warns(self):
        mesh = fx.merge(fx.box(0, 0, 0, 30, 30, 10), fx.box(40, 0, 0, 70, 30, 5))
        objs = fx.default_objects(meta={"ironing_type": "topmost"})
        _, r = fx.run(fx.build(objects=objs, meshes={"1": mesh}))
        msgs = [f["msg"] for f in F(r, "C12")]
        self.assertTrue(any("irons only the object's last layer" in m for m in msgs), msgs)
        self.assertEqual(r["objects_geometry"][0]["ironing_type_source"], "object")

    def test_cited_coupon_row_ok_and_bad_citation_warns(self):
        sheet = os.path.join(fx.WORK, "top_coupon_sheet.md")
        with open(sheet, "w", encoding="utf-8") as f:
            f.write("# top coupon\n")
        path = fx.build(meshes={"1": fx.box(0, 0, 0, 30, 30, 10)})
        _, r = fx.run(path, "--top-coupon-row", f"{sheet} tile 3")
        self.assertEqual(fx.levels(F(r, "C12")), {"OK"})
        _, r = fx.run(path, "--top-coupon-row", "trust me")
        self.assertTrue(any("not resolvable" in f["msg"] for f in F(r, "C12")))


class TestSupportTopZ(unittest.TestCase):
    def test_support_off_ok(self):
        _, r = fx.run(fx.build(), geometry=False)
        self.assertEqual(fx.levels(F(r, "C13")), {"OK"})

    def test_organic_prediction_and_not_verified(self):
        p = P(enable_support="1", support_type="tree(auto)", support_style="default", support_top_z_distance="0.25")
        _, r = fx.run(fx.build(proj=p), geometry=False)
        st = r["support_top_z"]
        self.assertEqual(st["resolved_style"], "tree_organic")
        self.assertEqual(st["predicted"]["0.2"]["gap"], 0.2)   # round(0.25 / 0.2) = 1 layer
        self.assertTrue(any(f["level"] == "WARN" and "NOT VERIFIED" in f["msg"] for f in F(r, "C13")))

    def test_hybrid_with_tower_forces_independent_off(self):
        p = P(enable_support="1", support_type="tree(auto)", support_style="tree_hybrid", support_top_z_distance="0.3",
              enable_prime_tower="1", independent_support_layer_height="1",
              filament_settings_id=["Bambu PLA Basic @BBL H2C"] * 2, filament_ids=["GFA00"] * 2,
              filament_colour=["#000000FF"] * 2, filament_type=["PLA"] * 2, filament_map=["2", "2"],
              textured_plate_temp=["55"] * 2, temperature_vitrification=["70"] * 2)
        objs = fx.default_objects()
        objs[0]["parts"].append({"id": "2", "subtype": "normal_part", "name": "inlay", "meta": {"extruder": "2"}, "uuid": "u-inlay"})
        _, r = fx.run(fx.build(proj=p, objects=objs, plates=fx.default_plates(maps="2 2")), geometry=False)
        st = r["support_top_z"]
        self.assertTrue(st["prime_tower_effective"])
        self.assertFalse(st["independent_effective"])
        self.assertEqual(st["predicted"]["0.2"]["gap"], 0.4)   # ceil(0.3 / 0.2) = 2 layers

    def test_scored_coupon_row_verifies(self):
        root = os.path.join(fx.WORK, "coupons")
        os.makedirs(root, exist_ok=True)
        sheet = os.path.join(root, "support_removal.md")
        with open(sheet, "w", encoding="utf-8") as f:
            f.write("## Result table - PLA Basic\n\n| step | Top Z | gap | il | sp | c | s | sag | sc | ss | pass/fail | ph | note | who |\n"
                    "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
                    "| A01 | 0.2 | 0.2 | 2 | 0.5 | 4 | 4 | 0 | 0 | 0 | pass | - | - | maker |\n"
                    "| A02 | 0.3 | 0.3 | 2 | 0.5 | | | | | | | | | |\n")
        p = P(enable_support="1", support_type="tree(auto)", support_style="default", support_top_z_distance="0.2")
        path = fx.build(proj=p)
        _, r = fx.run(path, "--coupon-root", root, "--top-z-coupon-row", f"{sheet} variant A01", geometry=False)
        self.assertEqual(fx.levels(F(r, "C13")), {"OK"}, F(r, "C13"))
        _, r = fx.run(path, "--coupon-root", root, "--top-z-coupon-row", f"{sheet} variant A02", geometry=False)
        self.assertTrue(any("not scored" in f["msg"] for f in F(r, "C13")))
        other = os.path.join(fx.WORK, "other_root")   # --coupon-root elsewhere: the sheet lies outside it
        _, r = fx.run(path, "--coupon-root", other, "--top-z-coupon-row", f"{sheet} variant A01", geometry=False)
        self.assertTrue(any("must lie under" in f["msg"] for f in F(r, "C13")))

    def tearDown(self):
        # main() stores --coupon-root in the module global COUPON_ROOT; restore the default for the other in-process tests
        audit_3mf.COUPON_ROOT = str(audit_3mf.mm_config.repo_root() / "work" / "coupons")


class TestMaterialAndPreset(unittest.TestCase):
    def test_c14_pla_and_petg_in_one_object_warns(self):
        p = P(filament_settings_id=["Bambu PLA Basic @BBL H2C", "Generic PETG @BBL H2C"], filament_ids=["GFA00", "GFG99"],
              filament_colour=["#000000FF", "#808080FF"], filament_type=["PLA", "PETG"], filament_map=["2", "2"],
              textured_plate_temp=["55", "70"], temperature_vitrification=["70", "80"])
        objs = fx.default_objects()
        objs[0]["parts"].append({"id": "2", "subtype": "normal_part", "name": "insert", "meta": {"extruder": "2"}, "uuid": "u-2"})
        _, r = fx.run(fx.build(proj=p, objects=objs, plates=fx.default_plates(maps="2 2")), geometry=False)
        c14 = F(r, "C14")
        self.assertEqual(fx.levels(c14), {"WARN"})
        self.assertIn("PLA and PETG bond weakly", c14[0]["msg"])

    def test_c14_one_family_ok_and_painting_warns(self):
        _, r = fx.run(fx.build(), geometry=False)
        self.assertEqual(fx.levels(F(r, "C14")), {"OK"})
        _, r = fx.run(fx.build(paint=True), geometry=False)
        self.assertTrue(any("colour painting" in f["msg"] for f in F(r, "C14")))

    def test_c15_default_preset_ok(self):
        _, r = fx.run(fx.build(), geometry=False)
        self.assertEqual(fx.levels(F(r, "C15")), {"OK"})

    def test_c15_other_preset_warns_reason_ok(self):
        p = P(print_settings_id="0.16mm High Quality @BBL H2C", layer_height="0.16")
        path = fx.build(proj=p)
        _, r = fx.run(path, geometry=False)
        self.assertEqual(fx.levels(F(r, "C15")), {"WARN"})
        _, r = fx.run(path, "--process-reason", "fine text needs 0.16 mm layers (sourced)", geometry=False)
        self.assertEqual(fx.levels(F(r, "C15")), {"OK"})
        _, r = fx.run(path, "--process-reason", "   ", geometry=False)   # blank counts as none
        self.assertEqual(fx.levels(F(r, "C15")), {"WARN"})

    def test_c15_edited_layer_height_warns(self):
        _, r = fx.run(fx.build(proj=P(layer_height="0.16")), geometry=False)
        self.assertEqual(fx.levels(F(r, "C15")), {"WARN"})
        self.assertIn("layer_height 0.16 mm in a preset named 0.20 mm", F(r, "C15")[0]["msg"])

    def test_c15_variable_layer_height_warns(self):
        _, r = fx.run(fx.build(layer_profile="0.2 0.2 5 0.12"), geometry=False)
        self.assertIn("variable layer height", F(r, "C15")[0]["msg"])


class TestStaleSlice(unittest.TestCase):
    def test_unsliced_ok(self):
        _, r = fx.run(fx.build(), geometry=False)
        self.assertEqual(fx.levels(F(r, "C16")), {"OK"})
        self.assertIn("unsliced", F(r, "C16")[0]["msg"])

    def test_consistent_slice_ok(self):
        p = P()
        _, r = fx.run(fx.build(proj=p, gcodes={1: fx.gcode(p)}, slice_info=fx.slice_info_xml()), geometry=False)
        self.assertEqual(fx.levels(F(r, "C16")), {"OK"}, F(r, "C16"))

    def test_md5_mismatch_warns(self):
        p = P()
        _, r = fx.run(fx.build(proj=p, gcodes={1: fx.gcode(p)}, md5="0" * 32, slice_info=fx.slice_info_xml()), geometry=False)
        self.assertEqual(fx.levels(F(r, "C16")), {"WARN"})
        self.assertIn("md5", F(r, "C16")[0]["msg"])

    def test_project_edited_after_slicing_warns(self):
        p = P()
        g = fx.gcode(p)
        _, r = fx.run(fx.build(proj=P(wall_loops="4"), gcodes={1: g}, slice_info=fx.slice_info_xml()), geometry=False)
        self.assertEqual(fx.levels(F(r, "C16")), {"WARN"})
        self.assertIn("wall_loops", F(r, "C16")[0]["msg"])

    def test_prediction_and_weight_mismatch_warn(self):
        p = P()
        _, r = fx.run(fx.build(proj=p, gcodes={1: fx.gcode(p)}, slice_info=fx.slice_info_xml(prediction="500", weight="9.9")),
                      geometry=False)
        msg = F(r, "C16")[0]["msg"]
        self.assertIn("prediction 500 s", msg)
        self.assertIn("weight 9.9 g", msg)

    def test_missing_gcode_and_object_mismatch_warn(self):
        _, r = fx.run(fx.build(slice_info=fx.slice_info_xml()), geometry=False)
        self.assertIn("is missing", F(r, "C16")[0]["msg"])
        p = P()
        _, r = fx.run(fx.build(proj=p, gcodes={1: fx.gcode(p)}, slice_info=fx.slice_info_xml(identify="999")), geometry=False)
        self.assertIn("identify_id", F(r, "C16")[0]["msg"])


class TestTextOutput(unittest.TestCase):
    def test_text_report_has_verdict(self):
        out = io.StringIO()
        with redirect_stdout(out):
            rc = audit_3mf.main(["audit_3mf.py", fx.build(), "--load-note", fx.load_note(), "--today", fx.TODAY, "--no-geometry"])
        text = out.getvalue()
        self.assertIn("VERDICT: WARN", text)
        self.assertIn("[OK] C7: L1:", text)
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
