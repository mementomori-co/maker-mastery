# Materials, texturing, rendering and lighting in Blender 5.2 LTS

Applies to: any printer (render-side only) - Blender 5.2 LTS manual (pinned `/manual/en/5.2/` pages)
Verified: 2026-10-04

## Facts

### Principled BSDF
- The Principled BSDF is a layered all-in-one shader based on the OpenPBR Surface model, with parameters compatible with Disney and Standard Surface style PBR shaders in other software. - [Principled BSDF](https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html)
- Base Color is the overall colour used for the diffuse, subsurface, metal and transmission parts. - [Principled BSDF](https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html)
- Metallic and Roughness are 0.0-1.0 inputs. The "0.0 to 1.0" wording on the page is a caption under example renders, but it matches the real input range. - [Principled BSDF](https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html)
- IOR: the body text says most materials sit between 1.0 (vacuum and air) and 4.0 (germanium); the default 1.5 approximates glass. - [Principled BSDF](https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html)
- Alpha controls surface transparency, with 1.0 fully opaque, and is usually linked to an Image Texture's Alpha output. - [Principled BSDF](https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html)
- Subsurface has four Method options (Christensen-Burley, Random Walk, Random Walk (Skin), Random Walk (Legacy)), all Cycles only; the manual says Random Walk (Legacy) will be deleted in the future. The "0 cm to 50 cm" figure next to Scale is an example-render caption, not a documented input range. - [Principled BSDF](https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html)
- Coat simulates a clearcoat, lacquer or car-paint layer on top, with Weight, IOR, Tint and its own Normal input. - [Principled BSDF](https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html)
- Sheen simulates very small surface fibres (a velvet-like edge reflection on cloth, or dust), with Roughness and Tint. - [Principled BSDF](https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html)
- Emission Strength 1.0 makes the object show exactly the Emission Color ("shadeless"). The "0.0 to 10.0" figure is an example-render caption; the page states no upper limit. - [Principled BSDF](https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html)

### Textures and colour space
- The Image Texture node has a Color Space setting that should match how the image file was saved. - [Image Texture](https://docs.blender.org/manual/en/5.2/render/shader_nodes/textures/image.html)
- Normal, bump and stencil maps hold data, not colour, and should be set to Non-Color so no colour conversion is applied. The list of colour spaces depends on the active OCIO config. - [Image Settings](https://docs.blender.org/manual/en/5.2/editors/image/image_settings.html)
- For tangent-space normal maps the UV coordinates must match and the image should be Non-Color. The page now lives under `shader_nodes/displacement/`; the old `vector/` path redirects there. - [Normal Map](https://docs.blender.org/manual/en/5.2/render/shader_nodes/displacement/normal_map.html)
- The Normal Map node's Space can be Tangent, Object or World. Its Convention option defaults to OpenGL (green channel Y points up); DirectX (Y down) suits maps from other software. - [Normal Map](https://docs.blender.org/manual/en/5.2/render/shader_nodes/displacement/normal_map.html)

### Material settings and EEVEE render method
- Material > Settings lists Pass Index and Viewport Display (Color, Metallic, Roughness) and links to separate EEVEE and Cycles settings sections. - [Material Settings](https://docs.blender.org/manual/en/5.2/render/materials/settings.html)
- EEVEE Render Method (Properties > Material > Settings; older EEVEE Legacy manuals called it Blend Mode): Dithered gives grayscale hashed transparency and works with render passes and raytracing (deferred); Blended gives coloured transparency but does not work with render passes or raytracing (forward). - [EEVEE Material Settings](https://docs.blender.org/manual/en/5.2/render/eevee/material_settings.html)

### Texture painting and baking
- Texture Paint is fastest with square power-of-two images (256, 512, 1024 and so on). - [Texture Paint introduction](https://docs.blender.org/manual/en/5.2/sculpt_paint/texture_paint/introduction.html)
- Cycles bake types: Combined, Ambient Occlusion (ignores all scene lights), Shadow, Position, Normal, UV, Roughness, Emit, Environment, Diffuse, Glossy, Transmission. Bake from Multires has its own types: Normals, Displacement, Vector Displacement. - [Baking](https://docs.blender.org/manual/en/5.2/render/cycles/baking.html)
- Baking to images adds a margin around UV islands by default, to avoid seams from texture filtering and mip-mapping; modes are Extend and Adjacent Faces, and Size is in pixels. - [Baking](https://docs.blender.org/manual/en/5.2/render/cycles/baking.html)
- Selected to Active baking uses Cage, Extrusion and Max Ray Distance; Max Ray Distance applies only when no cage is used. - [Baking](https://docs.blender.org/manual/en/5.2/render/cycles/baking.html)

### EEVEE vs Cycles
- EEVEE is the real-time engine, based on rasterization rather than path tracing; the manual says Cycles will always be more physically accurate. There is no `render/eevee/introduction.html` page; the index page is the entry point. - [EEVEE index](https://docs.blender.org/manual/en/5.2/render/eevee/index.html)
- EEVEE limitations include: lights have one colour and no light node trees; only single scattering; Blended materials do not work with post-process blur or raytracing; all BSDFs are approximations, so small differences from Cycles always remain. The page also says headless rendering is not supported on headless Windows systems. - [EEVEE limitations](https://docs.blender.org/manual/en/5.2/render/eevee/limitations/limitations.html)
- Cycles is Blender's physically based path tracer for production rendering. There is no `render/cycles/introduction.html` page; use the index. - [Cycles index](https://docs.blender.org/manual/en/5.2/render/cycles/index.html)

### Lights
- Light types are Point, Spot, Area and Sun. Temperature sets a blackbody colour in Kelvin. - [Light Object](https://docs.blender.org/manual/en/5.2/render/lights/light_object.html)
- Point, Spot and Area lights have Power (higher is brighter; negative values should be avoided); Sun lights have Strength. - [Light Object](https://docs.blender.org/manual/en/5.2/render/lights/light_object.html)
- With Normalize on, point, spot and area power is in Watts and sun strength in Watts per square metre. These are radiant Watts, not the electrical Watts printed on household bulbs. - [Light Object](https://docs.blender.org/manual/en/5.2/render/lights/light_object.html)
- The manual's real-world table (radiant W, Normalize on) includes: 800 lm LED bulb about 2.1 W (Point); 1000 lm bulb about 2.9 W (Point); candle about 0.05 W; 1500 lm PAR38 floodlight about 4 W (Area, Disk); 2500 lm fluorescent tube about 4.5 W (Area, Rectangle); 5000 lm car headlight about 22 W (Spot, 125 deg); clear sky about 1000 W/m2; cloudy sky about 500 W/m2; overcast sky about 200 W/m2; moonlight about 0.001 W/m2. It recommends adjusting Render > Film > Exposure, because eyes adapt and a render engine does not. - [Light Object](https://docs.blender.org/manual/en/5.2/render/lights/light_object.html)
- The Blackbody node turns a temperature in Kelvin into an RGB colour. It is filed under Color in the current manual; the old `shader_nodes/converter/blackbody.html` URL returns 404. - [Blackbody](https://docs.blender.org/manual/en/5.2/render/shader_nodes/color/blackbody.html)
- The World surface shader sets the background and environment light (colour, sky model or HDRI). For HDRI lighting use the Environment Texture node, not Image Texture, for correct mapping (Equirectangular or Mirror Ball). - [World](https://docs.blender.org/manual/en/5.2/render/lights/world.html)

### Colour management
- View transforms listed: Standard, ACES 1.3, ACES 2.0, Khronos PBR Neutral, AgX, Filmic, Filmic Log, False Color, Raw (the list depends on the bundled OCIO config). AgX offers 16.5 stops of dynamic range; Filmic is deprecated and superseded by AgX. - [Displays and Views](https://docs.blender.org/manual/en/5.2/render/color_management/displays_views.html)
- Exposure: output_value = render_value x 2^exposure. SDR sRGB is the display supported everywhere. - [Displays and Views](https://docs.blender.org/manual/en/5.2/render/color_management/displays_views.html)
- Colour management makes the pipeline interpret colours consistently across displays and is also where artistic look choices are made. - [Color Management](https://docs.blender.org/manual/en/5.2/render/color_management/index.html)
- Bit depth: OpenEXR stores float 16 or 32 bit; PNG stores 8 or 16 bit. The manual suggests OpenEXR for compositing or grading and PNG for on-screen output or video encoding. - [Image Formats](https://docs.blender.org/manual/en/5.2/files/media/image_formats.html)
- Rendered still sequences (PNG, or OpenEXR to keep HDR data) can be combined as an Image Strip in the Video Sequencer. - [Output properties](https://docs.blender.org/manual/en/5.2/render/output/properties/output.html)

### Cycles sampling and denoising
- Noise Threshold: typical values run from 0.1 to 0.001 (lower is cleaner and slower); 0 lets Cycles pick a value from the sample count. - [Sampling](https://docs.blender.org/manual/en/5.2/render/cycles/render_settings/sampling.html)
- Render (Max) Samples is the number of paths per pixel in the final render; more samples give a cleaner image and a longer render. - [Sampling](https://docs.blender.org/manual/en/5.2/render/cycles/render_settings/sampling.html)
- Denoiser: Automatic uses GPU denoising when supported and prefers OpenImageDenoise over OptiX; OpenImageDenoise typically gives the highest quality; OptiX needs an NVIDIA GPU configured in the Cycles Render Devices preferences. - [Sampling](https://docs.blender.org/manual/en/5.2/render/cycles/render_settings/sampling.html)

## In practice
- Treat every "X to Y" number next to a Principled BSDF field as a figure caption unless the body text states it as a limit. IOR's 1.0-4.0 is in the text; Subsurface Scale's 0-50 cm and Emission Strength's 0-10 are captions only.
- Set Color Space to Non-Color for every data texture: normal, bump, roughness, metallic and baked AO maps.
- Use the Environment Texture node for HDRI world lighting.
- For plausible light levels, keep Normalize on, start from the real-world power table, then adjust Render > Film > Exposure.
- Do not build a long-term look around Random Walk (Legacy) subsurface.
- Headless renders: see [blender-headless-render-cli.md](blender-headless-render-cli.md). Product lighting rules: see [product-render-lighting.md](product-render-lighting.md).

## Not verified / open questions
- The colour-space and view-transform lists depend on the OCIO config; another config can show a different list.
- Exactly which manual version switched from "Blend Mode" to "Render Method" wording was not traced.
- GPU and driver support for Cycles on your own machine is not covered here; check the GPU Rendering page linked in [blender-headless-render-cli.md](blender-headless-render-cli.md).

Sources:
- https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html - Principled BSDF inputs
- https://docs.blender.org/manual/en/5.2/render/shader_nodes/textures/image.html - Image Texture node and Color Space
- https://docs.blender.org/manual/en/5.2/editors/image/image_settings.html - Non-Color rule; OCIO-dependent list
- https://docs.blender.org/manual/en/5.2/render/shader_nodes/displacement/normal_map.html - Normal Map Space and Convention
- https://docs.blender.org/manual/en/5.2/render/materials/settings.html - Material > Settings panel
- https://docs.blender.org/manual/en/5.2/render/eevee/material_settings.html - EEVEE Render Method
- https://docs.blender.org/manual/en/5.2/sculpt_paint/texture_paint/introduction.html - power-of-two texture painting
- https://docs.blender.org/manual/en/5.2/render/cycles/baking.html - bake types, margin, Selected to Active
- https://docs.blender.org/manual/en/5.2/render/eevee/index.html - EEVEE overview
- https://docs.blender.org/manual/en/5.2/render/eevee/limitations/limitations.html - EEVEE limitations
- https://docs.blender.org/manual/en/5.2/render/cycles/index.html - Cycles overview
- https://docs.blender.org/manual/en/5.2/render/lights/light_object.html - light types, power units, real-world table
- https://docs.blender.org/manual/en/5.2/render/shader_nodes/color/blackbody.html - Blackbody node
- https://docs.blender.org/manual/en/5.2/render/lights/world.html - World and HDRI
- https://docs.blender.org/manual/en/5.2/render/color_management/displays_views.html - view transforms, exposure formula
- https://docs.blender.org/manual/en/5.2/render/color_management/index.html - colour management overview
- https://docs.blender.org/manual/en/5.2/files/media/image_formats.html - PNG and OpenEXR bit depths
- https://docs.blender.org/manual/en/5.2/render/output/properties/output.html - still sequences in the Video Sequencer
- https://docs.blender.org/manual/en/5.2/render/cycles/render_settings/sampling.html - Noise Threshold, Samples, Denoiser
