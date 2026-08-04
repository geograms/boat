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
- **Cabin** — the living superstructure on deck (5.3 × 2.28 m inside,
  1.85 m clear over the sole under a 200 mm structural roof).
- **Sole** — the interior floor inside the hull.
- **Roof terrace / sun deck** — the walkable top of the cabin roof
  (z 2 400). A sealed structural sandwich, so nothing above it can
  ever open the living quarters.
- **Walk-on glass** — laminated safety glass rated for foot traffic:
  here 6+6 mm heat-strengthened with an SGP interlayer and an
  anti-slip frit, in 8 panes of 1 200 × 1 050.
- **Air box** — the ventilated 60 mm gap between the bonded solar
  laminates and the glass over them. It keeps feet off the panels and
  keeps the cells cool; mesh slots fore and aft give the cross-flow.
- **Point load (design)** — the 2 kN on a 50 × 50 mm patch that sizes
  walk-on glass. Its stress grows with the LOG of the pane span, which
  is why smaller panes barely thin the glass.
- **Frit** — ceramic pattern fired onto the glass; here the anti-slip
  (R11) surface of the deck.
- **Air draft** — height from the waterline to the highest point:
  **2.27 m**.

## Interior (details in [interior.md](interior.md))

- **Sole** — the cabin floor (z 350). Everything heavy sits on it, not
  above it.
- **Settee berth** — a seat that is also a single bed: 1 900 × 620 each
  side of the dinette.
- **Dinette** — the saloon: two settee berths facing each other with a
  removable table between them; drop the table onto its bearers and the
  filler cushions make a second double.
- **Athwartships bed** — a bed lying ACROSS the boat. A 2 000 mm body
  fits the 2 280 mm beam, so the double eats only 1 400 mm of length.
- **Wetroom** — a heads compartment with no separate shower cubicle:
  the whole floor is the shower tray and drains to a sump.
- **Worktop / locker band** — galley counter at 900 and the run of
  lockers above it (1 450–2 200), only possible where there is no
  picture window.
- **Shelf band** — the 1 150–1 480 storage strip UNDER the window band
  in the living zones, where a locker would blind the saloon.
- **Air handler** — the indoor half of the AC heat pump, in the
  aft-starboard column beside the door, opposite its outside vent box.

## Stabilizer / hangar system

- **Float (floater, ama)** — one of the two 6.2 m outboard buoyancy
  bodies. Doubles as the road bogie: it carries the wheels ("the boat IS
  its own trailer" = the **hangar** concept).
- **Hangar** — Max's term for the integrated road-carriage function:
  floats + arms + wheels acting as the trailer and slipway carriage.
- **Arm** — rigid welded steel member connecting the hull to a float.
  Made of straight segments cut and welded at angles that follow the
  hull cross-section, so it nests against the hull in road pose.
- **Shoulder** — the arm's single pivot on the upper hull side
  (longitudinal axis) — the ONLY moving joint in the whole hangar arm.
  The rigid arm swings exactly 90° outboard from road to water pose.
- **Wrist (static)** — the welded arm-to-float connection at the arm
  tip. NOT a joint: the float is rigid on the arm; its roll follows
  the shoulder swing 1:1 (90° swing = side-to-flat).
- **Roll (float roll)** — the float's rotation about its own long axis:
  90° = on its side (road), 0° = flat on the water.
- **Jack-up stance** — the folded-arms-afloat configuration: floats
  65 % submerged carry the whole boat, hull keel awash and unloaded.
  The boat stands on its own floats (self-propelled by the waterjets;
  nothing external involved).
- **Pose / mode** — a named configuration of all movable parts: `road`,
  `launch`, `harbor`, `cruise`, `anchor`.
- **Reserve buoyancy** — the float volume above water available to
  resist heeling; sized to ~82 % of displacement per side (righting
  safety factor ≥ 3 vs a 50 kn gust).
- **Bevel (mating face)** — the 12° flat machined/molded on each float
  so it sits flush on the hull bottom in road pose (zero dead space).

## Aft entry (details in [aft_entry.md](aft_entry.md))

- **Companionway** — the boat-style entrance: sunken footwell, storm
  sill, a header you duck under, then full standing height inside.
- **Footwell / cockpit** — the sunken self-draining deck aft of the
  cabin; floor 360 mm above the waterline, scuppers through the
  transom. The hub for entering the boat and the balconies.
- **Storm sill (coaming)** — the 180 mm raised threshold under the
  door; water must rise over it to reach the living quarters.
- **Dogs** — the clamping latches that squeeze a gasketed door onto
  its frame.
- **Porch** — the fixed roof over the cockpit; its top is flush with
  the roof terrace, so it doubles as terrace floor.
- **Ship's ladder** — a stair steeper than ~45°, with stringers and
  nosed treads; the only thing that fits the aft deck's 720 mm run.
- **Boarding gate** — the gap left in the sheer rail (x 950–1450) with
  a threshold step, where you cross from the cockpit onto a balcony.
- **Folding handrail** — the ladder's single outboard rail; raised only
  when the roof terrace is in use, folded flat onto the stringer
  otherwise.

## Structure (details in [structure.md](structure.md))

- **Exoskeleton (space frame)** — external welded steel frame carrying
  every concentrated load (float arms, balconies, tow, fenders) so the
  hull skin only sees distributed water pressure.
- **Chassis rail** — the frame's main longitudinal tube at shoulder
  height, half-buried in the topsides (reads as a rubbing wale);
  carries the float-arm pins.
- **Sheer rail** — the frame's second longitudinal tube on the side-deck
  strip outside the cabin wall; carries the balcony hinges.
- **Ladder loop** — the frame's plan-view shape: two side rails closed
  by ties at bow and stern only. Transverse members amidships are
  impossible (no width outboard, floats underneath, cabin inside), so
  the loop plus the hull shell carries torsion.
- **Bow ring / stern ring** — the frame's end frames; the bow ring
  carries the tow-arch pivots, the stern ring the main waterjet.
- **Stern arch** — one wide A-arch on the transom, pin-locked in two
  poses: raised as a **gantry** (anchor sheave, winch fairlead, lights)
  at sea, or swung down-aft with a telescoping tongue as the
  **drawbar** on land. The boat tows stern-first.
- **Stem band** — the fixed external frame loop around the bow; the
  collision protection now that the arch lives aft.
- **Self-recovery winch** — 2 t electric winch on the stern tie; hauls
  the boat up a slipway when tyre grip alone is not enough.
- **Bulwark** — the raised sheer forward of the cabin standing above
  the closed foredeck plate.

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

## Road & regulation

- **StVZO envelope** — German road limits without special permit:
  width ≤ 2.55 m, height ≤ 4.0 m; the design's hard constraints.
- **Drawbar** — the fold-up A-frame at the bow with the ball coupling
  for the towing car.
- **Tempo-100** — German certification allowing 100 km/h trailer towing.
- **Slipway** — the concrete ramp used to drive the boat in/out of the
  water under its own wheel power (launch mode).
