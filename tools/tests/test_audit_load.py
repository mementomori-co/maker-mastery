r"""test_audit_load.py - audit_3mf.py check C7 (physical load record) on synthetic 3MF files and load notes.

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
import fixtures_3mf as fx  # noqa: E402  (sets MM_CONFIG / APPDATA before audit_3mf is imported)
import audit_3mf  # noqa: E402


def c7(r, rule=None):
    return fx.find(r, "C7", rule)


class TestLoadNote(unittest.TestCase):
    def test_all_rules_ok_when_loaded_as_sliced(self):
        rc, r = fx.run(fx.build(), geometry=False)
        rows = c7(r)
        self.assertEqual({f.get("rule") for f in rows}, {"L1", "L2", "L3", "L4", "L5", "L6", "L7"})
        self.assertEqual(fx.levels(rows), {"OK"}, [f["msg"] for f in rows if f["level"] != "OK"])
        slot1 = next(f["msg"] for f in c7(r, "L2") if "slot 1" in f["msg"])
        self.assertIn("used by filament 1", slot1)
        # C8 cannot find a profile on this isolated config: WARN, which makes the verdict WARN
        self.assertEqual(fx.levels(fx.find(r, "C8")), {"WARN"})
        self.assertEqual((rc, r["verdict"]), (1, "WARN"))

    def test_shipped_template_fails_l1_and_l3(self):
        note = os.path.join(fx.REPO, "knowledge", "00-gear-inventory", "current-load.md")
        self.assertTrue(os.path.isfile(note), note)
        rc, r = fx.run(fx.build(), note=note, geometry=False)
        self.assertEqual(fx.levels(c7(r, "L1")), {"FAIL"})
        self.assertEqual(fx.levels(c7(r, "L3")), {"FAIL"})
        self.assertEqual(fx.levels(c7(r, "L5")), {"FAIL"})   # every slot EMPTY: 0 loaded positions
        self.assertEqual((rc, r["verdict"]), (2, "FAIL"))

    def test_missing_note_is_one_fail(self):
        rc, r = fx.run(fx.build(), note=os.path.join(fx.WORK, "no-such-note.md"), geometry=False)
        rows = c7(r)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["level"], "FAIL")
        self.assertIn("MISSING", rows[0]["msg"])
        self.assertEqual(rc, 2)

    def test_note_without_verified_line_fails(self):
        _, r = fx.run(fx.build(), note=fx.load_note(verified=None), geometry=False)
        self.assertEqual(fx.levels(c7(r, "L1")), {"FAIL"})

    def test_stale_note_warns(self):
        _, r = fx.run(fx.build(), note=fx.load_note(verified="2025-12-01"), geometry=False)
        self.assertEqual(fx.levels(c7(r, "L1")), {"WARN"})
        self.assertIn("days old", c7(r, "L1")[0]["msg"])
        self.assertNotIn("FAIL", fx.levels(c7(r)))

    def test_future_note_warns(self):
        _, r = fx.run(fx.build(), note=fx.load_note(verified="2026-02-01"), geometry=False)
        self.assertEqual(fx.levels(c7(r, "L1")), {"WARN"})
        self.assertIn("future", c7(r, "L1")[0]["msg"])

    def test_bad_today_is_usage_error(self):
        err = io.StringIO()
        with redirect_stderr(err), redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as cm:
            audit_3mf.main(["audit_3mf.py", fx.build(), "--today", "10/01/2026"])
        self.assertEqual(cm.exception.code, 2)
        self.assertIn("not a YYYY-MM-DD date", err.getvalue())

    def test_unknown_slot_warns(self):
        rows = list(fx.GOOD_ROWS)
        rows[1] = ("H2C - AMS 2 Pro slot 2 (RIGHT inlet)", "not reported", "-")
        _, r = fx.run(fx.build(), note=fx.load_note(rows), geometry=False)
        unk = [f for f in c7(r, "L2") if "slot 2" in f["msg"]]
        self.assertEqual(len(unk), 1)
        self.assertEqual(unk[0]["level"], "WARN")
        self.assertIn("unknown", unk[0]["msg"])

    def test_bold_product_with_unknown_marker_is_loaded(self):
        rows = list(fx.GOOD_ROWS)
        rows[0] = ("H2C - AMS 2 Pro slot 1 (RIGHT inlet)", "**Bambu PLA Basic, Black** (mass unknown)", "label")
        _, r = fx.run(fx.build(), note=fx.load_note(rows), geometry=False)
        self.assertEqual(fx.levels(c7(r, "L3")), {"OK"})
        self.assertEqual(fx.levels(c7(r, "L5")), {"OK"})

    def test_middle_dot_separator_still_read(self):
        rows = [(a.replace("H2C - ", "H2C · "), b, c) for a, b, c in fx.GOOD_ROWS]
        _, r = fx.run(fx.build(), note=fx.load_note(rows), geometry=False)
        self.assertEqual(fx.levels(c7(r)), {"OK"})

    def test_product_not_loaded_fails_l3_l4_l5(self):
        p = fx.project(filament_settings_id=["Bambu PLA Basic @BBL H2C", "Bambu PLA Matte @BBL H2C"], filament_ids=["GFA00", "GFA01"],
                       filament_colour=["#000000FF", "#FFFFF0FF"], filament_type=["PLA", "PLA"], filament_vendor=["Bambu Lab"] * 2,
                       filament_map=["2", "2"], textured_plate_temp=["55", "55"], temperature_vitrification=["70", "70"])
        rc, r = fx.run(fx.build(proj=p, plates=fx.default_plates(maps="2 2")), geometry=False)
        l3 = c7(r, "L3")
        self.assertTrue(any(f["level"] == "OK" and f.get("filament") == 1 for f in l3))
        self.assertTrue(any(f["level"] == "FAIL" and f.get("filament") == 2 and "'Bambu PLA Matte' is not loaded" in f["msg"] for f in l3))
        self.assertEqual(fx.levels(c7(r, "L5")), {"FAIL"})
        self.assertEqual((rc, r["verdict"]), (2, "FAIL"))

    def test_other_catalogue_colour_of_same_line_fails_l4(self):
        p = fx.project(filament_colour=["#FFFFFFFF"])   # Jade White in the synthetic catalogue, but Black is loaded
        _, r = fx.run(fx.build(proj=p), geometry=False)
        l4 = c7(r, "L4")
        self.assertEqual(fx.levels(l4), {"FAIL"})
        self.assertIn("different spool", l4[0]["msg"])

    def test_custom_colour_warns_l4(self):
        _, r = fx.run(fx.build(proj=fx.project(filament_colour=["#123456FF"])), geometry=False)
        self.assertEqual(fx.levels(c7(r, "L4")), {"WARN"})
        self.assertEqual(fx.levels(c7(r, "L3")), {"OK"})

    def test_wrong_filament_id_fails_l3(self):
        _, r = fx.run(fx.build(proj=fx.project(filament_ids=["GFA99"])), geometry=False)
        self.assertEqual(fx.levels(c7(r, "L3")), {"FAIL"})

    def test_third_party_matches_on_vendor_and_type(self):
        rows = list(fx.GOOD_ROWS)
        rows[0] = ("H2C - AMS 2 Pro slot 1 (RIGHT inlet)", "**Acme PETG, Grey**", "spool label")
        p = fx.project(filament_settings_id=["Generic PETG @BBL H2C"], filament_ids=["GFG99"], filament_type=["PETG"],
                       filament_vendor=["Acme"], filament_colour=["#808080FF"], textured_plate_temp=["70"])
        _, r = fx.run(fx.build(proj=p), note=fx.load_note(rows), geometry=False)
        self.assertEqual(fx.levels(c7(r, "L3")), {"OK"})
        self.assertIn("third-party", c7(r, "L3")[0]["msg"])
        self.assertEqual(fx.levels(c7(r, "L4")), {"WARN"})
        # another vendor does not match
        p2 = dict(p, filament_vendor=["Other"])
        _, r2 = fx.run(fx.build(proj=p2), note=fx.load_note(rows), geometry=False)
        self.assertEqual(fx.levels(c7(r2, "L3")), {"FAIL"})

    def test_plate_map_on_wrong_side_fails_l6(self):
        _, r = fx.run(fx.build(plates=fx.default_plates(maps="1")), geometry=False)
        self.assertEqual(fx.levels(c7(r, "L6")), {"FAIL"})

    def test_auto_mode_without_left_spool_fails_l6(self):
        p = fx.project(filament_map_mode="Auto For Flush")
        _, r = fx.run(fx.build(proj=p, plates=fx.default_plates(mode="Auto For Flush")), geometry=False)
        self.assertEqual(fx.levels(c7(r, "L6")), {"FAIL"})
        self.assertIn("no LEFT spool recorded", c7(r, "L6")[0]["msg"])

    def test_cli_quirk_reads_gcode_mode(self):
        p = fx.project()
        g = fx.gcode(p, map_mode="Manual")
        path = fx.build(proj=p, plates=fx.default_plates(mode="Auto For Flush"), gcodes={1: g})
        _, r = fx.run(path, geometry=False)
        l6 = c7(r, "L6")
        self.assertEqual(fx.levels(l6), {"OK"}, l6)
        self.assertIn("CLI quirk", l6[0]["msg"])
        g2 = fx.gcode(p, map_mode="Auto For Flush")
        _, r2 = fx.run(fx.build(proj=p, plates=fx.default_plates(mode="Auto For Flush"), gcodes={1: g2}), geometry=False)
        self.assertEqual(fx.levels(c7(r2, "L6")), {"FAIL"})

    def test_sliced_gcode_map_other_side_fails_l6(self):
        p = fx.project()
        _, r = fx.run(fx.build(proj=p, gcodes={1: fx.gcode(p, fil_map="1")}), geometry=False)
        l6 = c7(r, "L6")
        self.assertEqual(fx.levels(l6), {"FAIL"})
        self.assertIn("G-code '; filament_map = 1'", l6[0]["msg"])

    def test_other_plate_fails_l7(self):
        rows = list(fx.GOOD_ROWS)
        rows[3] = ("H2C - plate on the bed", "Smooth PEI", "looked")
        _, r = fx.run(fx.build(), note=fx.load_note(rows), geometry=False)
        self.assertEqual(fx.levels(c7(r, "L7")), {"FAIL"})

    def test_unconfirmed_plate_warns_l7(self):
        rows = list(fx.GOOD_ROWS)
        rows[3] = ("H2C - plate on the bed", "Textured PEI (not re-confirmed)", "earlier note")
        _, r = fx.run(fx.build(), note=fx.load_note(rows), geometry=False)
        self.assertEqual(fx.levels(c7(r, "L7")), {"WARN"})
        self.assertIn("not physically confirmed", c7(r, "L7")[0]["msg"])

    def test_no_plate_row_warns_l7(self):
        _, r = fx.run(fx.build(), note=fx.load_note(fx.GOOD_ROWS[:3]), geometry=False)
        self.assertEqual(fx.levels(c7(r, "L7")), {"WARN"})


class TestPrinterKey(unittest.TestCase):
    def test_printer_key(self):
        self.assertEqual(audit_3mf.printer_key("Bambu Lab H2C 0.4 nozzle"), "H2C")
        self.assertEqual(audit_3mf.printer_key("Bambu Lab P1S 0.4 nozzle"), "P1S")
        self.assertEqual(audit_3mf.printer_key("Bambu Lab X1C 0.4 nozzle"), "X1C")
        self.assertEqual(audit_3mf.printer_key("Bambu Lab A1 mini 0.4 nozzle"), "A1 mini")
        self.assertIsNone(audit_3mf.printer_key("Some Other Printer"))

    def test_row_is(self):
        self.assertTrue(audit_3mf._row_is("H2C - AMS 2 Pro slot 1", "H2C"))
        self.assertTrue(audit_3mf._row_is("H2C · AMS 2 Pro slot 1", "H2C"))
        self.assertTrue(audit_3mf._row_is("A1 mini - AMS lite slot 1", "A1 mini"))
        self.assertFalse(audit_3mf._row_is("A1 mini - AMS lite slot 1", "A1"))
        self.assertTrue(audit_3mf._row_is("X1C - AMS slot 2", "X1C"))
        self.assertFalse(audit_3mf._row_is("X1C - AMS slot 2", "H2C"))
        self.assertFalse(audit_3mf._row_is("H2CX - AMS", "H2C"))

    def test_other_printer_rows_found(self):
        p = fx.project(printer_settings_id="Bambu Lab A1 mini 0.4 nozzle", printer_model="Bambu Lab A1 mini",
                       print_settings_id="0.20mm Standard @BBL A1M", default_print_profile="0.20mm Standard @BBL A1M",
                       filament_settings_id=["Bambu PLA Basic @BBL A1M"], nozzle_diameter=["0.4"], filament_map=["1"])
        rows = [("A1 mini - AMS lite slot 1", "**Bambu PLA Basic, Black**", "looked"),
                ("A1 - AMS slot 1", "**Bambu PLA Basic, Jade White**", "a row of another printer"),
                ("A1 mini - plate on the bed", "Textured PEI", "looked")]
        _, r = fx.run(fx.build(proj=p, plates=fx.default_plates(maps="1")), note=fx.load_note(rows), geometry=False)
        l2 = c7(r, "L2")
        self.assertEqual(len(l2), 1, l2)   # only the A1 mini row, not the A1 row
        self.assertEqual(fx.levels(c7(r, "L3")), {"OK"})
        self.assertEqual(fx.levels(c7(r, "L7")), {"OK"})
        self.assertEqual(c7(r, "L6"), [])   # the side check is H2C only


if __name__ == "__main__":
    unittest.main()
