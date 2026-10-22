# Product render lighting and camera in Blender 5.2 (Cycles)

Applies to: any printer (render-side only) - Blender 5.2 LTS manual (pinned `/manual/en/5.2/` pages)
Verified: 2026-10-20

## Facts
- Larger lights give softer shadows and highlights and look dimmer, because the same power spreads over a larger area. Point and Spot lights have Radius; Area lights have Size (or Size X / Size Y) and the shapes Rectangle, Square, Disk and Ellipse. - [Light Objects](https://docs.blender.org/manual/en/5.2/render/lights/light_object.html)
- Area lights cast shadows with soft borders; point-like lights cast sharp ones. - [Light Objects](https://docs.blender.org/manual/en/5.2/render/lights/light_object.html)
- Normalize (on by default) keeps total power constant when a light's size or shape changes; with it off, a bigger light emits more. - [Light Objects](https://docs.blender.org/manual/en/5.2/render/lights/light_object.html)
- Per-light Exposure multiplies the light's intensity by 2^exposure. - [Light Objects](https://docs.blender.org/manual/en/5.2/render/lights/light_object.html)
- With Normalize on, Power is radiant flux in Watts (sun: W/m2), not electrical Watts. Table examples: 1500 lm PAR38 floodlight = 4 W Area Disk; 2500 lm fluorescent tube = 4.5 W Area Rectangle. The manual notes these can look too bright or dim because eyes adapt; compensate with Render > Film > Exposure. - [Light Objects](https://docs.blender.org/manual/en/5.2/render/lights/light_object.html)
- Cycles Area light Spread: large values give soft light; small values give sharper light, which the manual likens to a gridded softbox. - [Cycles Light Settings](https://docs.blender.org/manual/en/5.2/render/cycles/light_settings.html)
- Multiple Importance Sample: lights use direct light sampling by default, which can be noisy for area lights and sharp glossy reflections; enabling MIS adds indirect sampling to cut that noise. The page places it at Properties > Object Data > Settings. - [Cycles Light Settings](https://docs.blender.org/manual/en/5.2/render/cycles/light_settings.html)
- Lights are not directly visible in renders. Light shader nodes (for example a texture varying colour across a light) work in Cycles only; EEVEE ignores them. - [Cycles Light Settings](https://docs.blender.org/manual/en/5.2/render/cycles/light_settings.html)
- View transforms: AgX improves on Filmic, has 16.5 stops of range and desaturates very bright colours; Filmic is deprecated. Khronos PBR Neutral targets well-exposed product shots where HDR values are mostly small highlights, and assumes grey-scale lighting. ACES 1.3 is listed as suitable for photoreal results; ACES 2.0 is more neutral with gentler highlight rolloff. Standard is often used for non-photoreal work or video editing. - [Displays and Views](https://docs.blender.org/manual/en/5.2/render/color_management/displays_views.html)
- The False Color view is a heat map of normalised linear intensity after Color Management Exposure. Bands include Low Clip (black), 5-16 % green-cyan, 16-22 % grey, 22-35 % green-yellow, 80-97 % red, High Clip (white). The manual names no target band. - [Displays and Views](https://docs.blender.org/manual/en/5.2/render/color_management/displays_views.html)
- Color Management Exposure (stops) is applied as output = render x 2^exposure before colour conversion, and it is part of the view applied to displayed and saved renders, so it is baked into PNG and JPEG output and left out only of linear EXR data. Cycles Film Exposure instead works on the render data. - [Displays and Views](https://docs.blender.org/manual/en/5.2/render/color_management/displays_views.html), [Film](https://docs.blender.org/manual/en/5.2/render/cycles/render_settings/film.html)
- Film filter Width: lower is crisper, higher is softer with less aliasing. Film Transparent renders the background transparent for compositing. - [Film](https://docs.blender.org/manual/en/5.2/render/cycles/render_settings/film.html)
- Camera depth of field: a Focus Object overrides the focus distance; a lower F-Stop gives stronger blur; bokeh needs at least 3 aperture blades. - [Cameras](https://docs.blender.org/manual/en/5.2/render/cameras.html)
- Principled BSDF: Roughness 0.0 is a perfectly sharp reflection and 1.0 diffuse; Transmission covers specular reflection and refraction; IOR 1.5 approximates glass (not any specific filament); Subsurface suits skin, milk or wax, with Weight 0.0-1.0 ("typically" 0 or 1) and Radius as the average scatter distance. - [Principled BSDF](https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html)
- Light Paths: the manual says total max bounces should be at the maximum for best quality; 0 bounces is direct light only; Transmission and other bounce types have their own limits; clamping removes fireflies but also dims other bright lights and reflections. - [Light Paths](https://docs.blender.org/manual/en/5.2/render/cycles/render_settings/light_paths.html)

## In practice
- Set softness with light Size (Area) or Radius (Point/Spot), then restore brightness with Power or by turning Normalize off. Power does not change softness.
- Judge exposure in the False Color view and write down the Color Management Exposure value with each reading, because the bands depend on it.
- For a backlit or glowing part, compare AgX against Khronos PBR Neutral: AgX desaturates bright colour by design, and PBR Neutral assumes grey-scale lighting.
- Measure key-to-fill at the part by rendering key-only and fill-only passes, not by reading the Exposure sliders.

## Not verified / open questions
- Overreach, not a fact: "N stops of Exposure offset equals N stops of key-to-fill at the part". It holds for emitted output only; distance, size and angle also count, and the photographic lighting ratio is (key + fill) : fill.
- Overreach: "an Area Rectangle is a softbox". The manual's examples are a window, neon lights and a TV screen; softbox is an analogy.
- Overreach: "Spread limits spill onto the background". The manual says only that low Spread simulates a gridded softbox.
- Overreach: "enable MIS on every Area light". The manual ties the noise benefit to area lights and sharp glossy reflections; a satin part is not sharp-glossy.
- Overreach: "the table's Watts are for room-scale lights only". Not in the manual; Power is total radiant output at any distance.
- Overreach: "translucent PETG = Transmission plus Roughness". That is a shading choice; no satin roughness, PETG IOR or subsurface radius is sourced here.
- No bounce count per wall count, macro F-Stop value or gradient-card (texture on a light) recipe is sourced.

Sources:
- https://docs.blender.org/manual/en/5.2/render/lights/light_object.html - light size and softness, Area shapes, Normalize, Exposure, power units and table
- https://docs.blender.org/manual/en/5.2/render/cycles/light_settings.html - Spread, MIS, light visibility, light shader nodes
- https://docs.blender.org/manual/en/5.2/render/color_management/displays_views.html - view transforms, False Color, exposure formula and baking
- https://docs.blender.org/manual/en/5.2/render/cycles/render_settings/film.html - Film Exposure, filter Width, Transparent
- https://docs.blender.org/manual/en/5.2/render/cameras.html - Focus Object, F-Stop, aperture blades
- https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html - Roughness, Transmission, IOR, Subsurface
- https://docs.blender.org/manual/en/5.2/render/cycles/render_settings/light_paths.html - bounces and clamping
