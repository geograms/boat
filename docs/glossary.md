# Glossary — Boat-Home Project

Shared language for the design. Geometry values live in
`freecad/params.py`; this file defines the *words*.

## Hull & structure

- **Hull** — the main watertight body (Dutch-barge style: bluff rounded
  bow, full midbody, near-vertical sides, flat-ish bottom). 7.20 m long,
  2.50 m wide.
- **Dutch barge** — traditional Netherlands canal workboat shape the hull
  imitates; maximizes interior volume at shallow draft.
- **Station** — a numbered cross-section of the hull at a given length
  position; the hull surface is lofted through the stations.
- **Chine** — the hard edge where the hull bottom meets the hull side.
- **Deadrise** — the slope of the hull bottom from keel to chine (~12°).
- **Keel / keel line** — the centerline bottom of the hull; z = 0 datum.
- **Sheer / gunwale** — the top edge of the hull side, where deck meets
  topsides. The arm shoulders and balcony hinges mount here.
- **Transom** — the flat aft (rear) end of the hull; x = 0 datum.
- **Waterline (WL)** — the level water reaches on the hull at rest
  (260 mm above keel at ~2.0 t displacement).
- **Displacement** — the weight of water the hull pushes aside = the
  boat's floating weight.
- **Freeboard** — hull height above the waterline.
- **Cabin** — the living superstructure on deck (5.3 × 2.4 m, 1.8 m
  standing headroom over the sole).
- **Sole** — the interior floor inside the hull.
- **Pop-top canopy / solar roof** — the raisable roof slab carrying six
  solar panels; lifts 1.5 m on four posts at anchor to create the
  **chillout deck** (roof terrace).

## Stabilizer / hangar system

- **Float (floater, ama)** — one of the two 6.2 m outboard buoyancy
  bodies. Doubles as the road bogie: it carries the wheels ("the boat IS
  its own trailer" = the **hangar** concept).
- **Hangar** — Max's term for the integrated road-carriage function:
  floats + arms + wheels acting as the trailer and slipway carriage.
- **Arm** — rigid welded steel member connecting the hull to a float.
  Made of straight segments cut and welded at angles that follow the
  hull cross-section, so it nests against the hull in road pose.
- **Shoulder** — the arm's single pivot on the gunwale (longitudinal
  axis). The whole arm swings ~71° outboard from road to water pose.
- **Wrist** — the pivot at the arm tip where the float attaches; rolls
  the float 90° between poses.
- **Roll (float roll)** — the float's rotation about its own long axis:
  90° = on its side (road), 0° = flat on the water.
- **Pose / mode** — a named configuration of all movable parts: `road`,
  `launch`, `harbor`, `cruise`, `anchor`, `foiling`.
- **Reserve buoyancy** — the float volume above water available to
  resist heeling; sized to ~82 % of displacement per side (righting
  safety factor ≥ 3 vs a 50 kn gust).
- **Bevel (mating face)** — the 12° flat machined/molded on each float
  so it sits flush on the hull bottom in road pose (zero dead space).

## Wheels & drive (details in [wheels.md](wheels.md))

- **Caster mounting** — wheels on stub axles perpendicular to the float
  deck; this makes wheels vertical when the float is on its side (road)
  and flat on the deck when the float is level (water).
- **Stub axle** — short fixed shaft carrying one wheel; no through-axle.
- **Wheel well** — recess in the float deck the wheel disc half-sinks
  into.
- **Wheel cover / fender cover** — low lid over each flat-lying wheel in
  water pose, open on the outboard side so the tire edge stays exposed.
- **Rolling fender** — the exposed tire edge standing proud of the hull
  in harbor pose; touches the quay wall first and rolls as the boat
  surges, protecting the hull.
- **Machinery bay** — watertight compartment inside each float housing
  the electric motor + hydraulic pump + valve manifold; gasketed deck
  hatch above it.
- **Orbital motor (gerotor)** — the hydraulic wheel-hub motor type:
  oil-filled, natively submersible, high torque at low rpm.
- **Electric-over-hydraulic** — the drive architecture: electricity
  crosses the joints (one 48 V cable), hydraulics stay entirely inside
  the float.
- **Wet-mate connector** — an electrical connector rated to be plugged/
  unplugged and operated underwater.
- **Skid steering** — steering by running left and right floats' wheels
  at different speeds; no steered axle.
- **Tongue load** — the downward weight on the car's tow hitch (~100 kg).
- **Track** — distance between left and right wheel contact patches
  (2 270 mm).
- **Wheelbase** — distance from front to rear axle (3 400 mm).

## Solar & energy

- **Panel (module)** — one flexible solar laminate, 1700 × 1130 × 4 mm,
  ~430 W, ~6 kg. Same footprint everywhere on the boat (12 total).
- **Bifacial** — a panel producing power from both faces; used on the
  balconies (rear face harvests light reflected off the water).
- **Solar balcony** — fold-down panel deck hinged at the gunwale:
  horizontal walkway over the floats in water pose (resting on legs on
  the wheel covers), folded up over the windows on road.
- **Shutter (storm shutter)** — the balcony in its folded-up road/harbor
  position, covering the window band while still charging.
- **House bank** — the 48 V LiFePO₄ battery bank feeding drive, canopy
  actuators, and domestic loads.

## Propulsion (details in [propulsion.md](propulsion.md))

- **Rim drive (rim-driven thruster)** — propulsor whose blades are
  carried by a motor ring at their tips: no shaft, no hub, open center;
  flooded sealed stator, natively submersible.
- **Tunnel** — the bore through the float tail (or nacelle) the thruster
  sits in; protects the rotor and carries the intake grilles.
- **Weed rake / trash rack** — intake bars raked 45° aft so flow pushes
  debris along and off them instead of pinning it (hydro-plant term).
- **Reverse flush** — brief full-reverse burst that ejects debris from
  the tunnel and grille ("weed button").
- **Differential thrust** — steering by running the two float thrusters
  at different speeds/directions; replaces a rudder at low speed.
- **Nacelle** — the streamlined housing of the main thruster behind the
  transom.

## Hydrofoil

- **Hydrofoil / foil** — underwater wing that lifts the bow at speed
  (partial lift / semi-foiling).
- **Strut** — the vertical blade connecting hull to foil wing; raked
  15° aft.
- **Rake** — the aft lean of the strut; makes ground strikes glance and
  kick the foil back instead of snapping it.
- **Wet case / trunk** — the watertight box the foil retracts into; its
  walls end above the waterline so no moving seal is needed.
- **Keel slot + flush doors** — the opening in the hull bottom the strut
  passes through, closed by fairing doors when retracted.
- **Wing recess** — the shaped pocket in the hull bottom the retracted
  foil wing nests into, flush, for shallow water.
- **Lead screw (drive)** — the threaded shaft that raises/lowers the
  foil; mounted dry above the wet case (Max's "spiral on a tube",
  relocated above the waterline).
- **Shear pin** — sacrificial pin that breaks at overload, letting the
  foil kick back in a grounding instead of destroying the structure.

## Road & regulation

- **StVZO envelope** — German road limits without special permit:
  width ≤ 2.55 m, height ≤ 4.0 m; the design's hard constraints.
- **Drawbar** — the fold-up A-frame at the bow with the ball coupling
  for the towing car.
- **Tempo-100** — German certification allowing 100 km/h trailer towing.
- **Slipway** — the concrete ramp used to drive the boat in/out of the
  water under its own wheel power (launch mode).
