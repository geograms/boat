# Road Approval — Homologating the Hangar

Status: research, August 2026. Everything here is desk research from
public sources; **none of it is a binding quote**. The one number that
matters — what a technical service will actually charge to approve
*this* vehicle — can only come from a paid pre-assessment, and §9 says
how to buy one.

The question: the running gear (the "hangar" — two floats carrying six
wheels on swinging arms) is **part of the boat**, not a separate
trailer. So what is being registered, and how hard is it?

---

## 1. What is actually being approved

Three separate approvals, easily confused:

| | What | Who | Status here |
|---|---|---|---|
| **A** | the **vehicle** — road-legal on German/EU roads | IMT / KBA / RDW via a technical service | **the subject of this document** |
| **B** | the **boat** — CE marking under the Recreational Craft Directive 2013/53/EU | self-certification (cat. C < 12 m or cat. D) | self-build for own use is **exempt for 5 years** (§8) |
| **C** | the **waterway registration** — boat number, licences, insurance | WSA / national authority | routine, not covered here |

Only **A** is hard.

## 2. The fork in the road: trailer or amphibian

This decides everything, and it is a **design decision, not a legal
one**.

**Category O trailer** (O2: 750–3 500 kg) is the easy branch. A trailer
has no requirements for engine, emissions, steering or driver
controls. The list is short: brakes, lights, coupling, frame, masses,
dimensions, underrun protection, mudguards.

**Motor vehicle / amphibian** is the hard branch. The moment the
vehicle propels itself on a public road at road speed, it becomes a
motor vehicle needing whole-vehicle requirements — and amphibians are
worse than that, because German practice has an unresolved conflict:
road vehicles carry a Kfz registration under StVZO, boats carry a
different marking under the waterways rules, and **dual marking is not
provided for**. Water authorities have refused boat numbers to vehicles
already marked as motor vehicles, and the water police have refused to
accept car plates as boat marking. That fight is not one to pick.

**The Sealander precedent is exactly on point.** The Sealander swimming
caravan is registered as an unbraked caravan trailer *and* as a
category D motorboat. A Swiss court held it is **not** an amphibious
vehicle — expressly because it **has no drive of its own**. Its status
comes from *not* driving itself on the road.

### The design rule that follows

> **On the road, the wheel drive must be incapable of exceeding 6 km/h.**

German vehicle registration law (FZV) applies to motor vehicles with a
design speed **over 6 km/h**. At or below 6 km/h the drive is a
manoeuvring aid — legally the same family as the caravan movers sold by
the thousand — and the vehicle stays a trailer. The current design
targets ≤ 10 km/h on land; **drop it to 6 km/h and the whole approval
problem changes category.** That is a firmware limit plus a mechanical
one the inspector can verify, and it costs nothing on a slipway, where
6 km/h is already faster than anyone should be reversing a 2.5 t boat
down a ramp.

Slipway and yard use off the public road is unaffected — that is
private ground.

## 3. What the technical service will actually look at

Not the boat. The boat is just "the body". The file is about the
running gear:

| Item | What has to be shown | Difficulty |
|---|---|---|
| **Service brake** | > 750 kg ⇒ a braking system to UN R13; in Europe that means an **overrun (inertia) brake** — coupling head, transmission, wheel brakes, with a **brake calculation** matching axle, brake and overrun device | **the hard one — §4** |
| **Breakaway cable** | standard part with the coupling | trivial |
| **Coupling / drawbar** | E-marked coupling, D-value ≥ the combination, drawbar strength | easy if bought |
| **Arms locked in road position** | a **positive mechanical lock** per arm — not hydraulic pressure — plus a strength calculation for arm, shoulder pin and lock | **the "hangar" question — §5** |
| **Axles / suspension** | load rating covering the axle load, with the manufacturer's papers | easy if bought |
| **Lighting** | E-marked lamps, rear **triangular** reflectors (trailers only), side markers, plate light | easy |
| **Rear underrun protection, mudguards, spray suppression** | standard fittings | easy |
| **Masses and dimensions** | ≤ 2 550 mm wide, ≤ 4 000 mm high; axle loads; nose weight; a weighing | already asserted in `params.py` |
| **VIN** | assigned by the approval authority for a new build | small fee |

## 4. The brake is the real obstacle, not the hangar

This is the finding that matters most, and it is an **engineering**
problem the current design does not yet solve.

An overrun brake works mechanically: the trailer runs onto the coupling
head, a linkage pulls the wheel brakes. The approval is granted to the
**combination** of overrun device + axle + brake, and the makers
(Knott, AL-KO, BPW) supply the matching brake calculation free with
their parts. Deviate from a catalogue combination and you are asking a
technical service to accept an unproven brake system on a 2 t trailer —
which is where a €500 inspection turns into a five-figure test
programme.

Our six wheels sit on **swinging arms inside the floats**, driven
hydraulically. There is no catalogue axle to buy. Options, cheapest
first:

1. **Hydraulic overrun brakes.** The overrun device drives a master
   cylinder; hydraulic lines run out to wheel cylinders on the drums.
   This is standard on boat trailers, so certified components exist,
   and hydraulic lines survive the arm's 90° swing where a mechanical
   Bowden linkage would not. **This is the route to design for.**
2. **Brake only the middle wheels** (one "axle" pair per side) and
   carry the rest as unbraked. Braking rate still has to be met, so
   this needs the calculation to close — check it early.
3. **Electric brakes** — common outside the EU, awkward inside it, and
   they need a controller in the towing car.
4. **Bespoke brake, tested.** Real UN R13 testing. Avoid.

**Action for the CAD model:** pick the overrun device, drum brakes and
wheel cylinders from one manufacturer's boat-trailer catalogue, size
the arms around them, and keep the papers. The brake decides the
running-gear geometry, not the other way round.

## 5. The hangar itself — less scary than it looks

A trailer whose axles fold away is unusual, not illegal. There is no
rule against a movable running gear; the requirement is that in the
road position it is **locked positively and provably**:

- a **pin or over-centre lock** per arm, engaging mechanically, so loss
  of hydraulic pressure cannot fold the gear;
- a strength calculation for the arm, the shoulder pin and the lock at
  the design axle load with the usual dynamic factor;
- ideally a **road-position indicator** the driver can see.

Expect the technical service to want the calculation stamped by an
engineer. That is normal for any one-off frame — self-built trailers
are routinely asked to show material certificates and welding
provenance, which is the same conversation.

## 6. Germany — the process

**There is no EU-wide route for a trailer.** EU individual vehicle
approval under Article 44 of Regulation (EU) 2018/858 exists only for
M1 and N1 (cars and small vans). Category O gets a **national
individual approval** only, under Article 45 — in German practice a
**Vollgutachten nach § 21 StVZO** or an **Einzelgenehmigung nach § 13
EG-FGV**, drawn up by an *amtlich anerkannter Sachverständiger* at
TÜV/DEKRA/GTÜ, then registered at the Zulassungsstelle.

Steps:

1. **Pre-assessment** with a technical service. Bring drawings, masses,
   the brake concept and the 6 km/h limitation. Ask them to state in
   writing what evidence they will require.
2. **Buy the certified parts** (brakes, coupling, lamps) and keep every
   approval sheet and brake calculation.
3. **Build**, documenting welds and materials.
4. **Full assessment** — the vehicle is presented physically, weighed,
   measured, brake-tested.
5. **VIN assignment**, then **registration** (Zulassung), plates,
   insurance.
6. Optional **Tempo 100** if you want to tow at 100 km/h.

### Cost and time, Germany

Published prices are for ordinary vehicles; this one is not ordinary.
The bands below are **my estimate**, built from the published ranges
plus the extra evidence this vehicle will attract:

| | Low | High | Note |
|---|---|---|---|
| Pre-assessment / consultation | 300 | 800 | buy this first — it prices everything else |
| Engineering: arm, pin, lock, frame calculations | 1 000 | 4 000 | stamped; less if you produce the FEA yourself |
| Certified brake, coupling, lighting parts | 800 | 2 500 | hardware, would be bought anyway |
| Full assessment (§ 21 / § 13 EG-FGV) | 400 | 1 500 | published einzelabnahme range is 80–500 for normal work; this is not normal work |
| VIN assignment + registration + plates | 150 | 250 | published: ≈ €20 VIN, ≈ €123 registration |
| Contingency: re-inspection, extra evidence | 500 | 3 000 | assume at least one iteration |
| **Total** | **≈ 3 150** | **≈ 12 050** | |

**Elapsed time: 4–10 months** from first meeting to plates, most of it
waiting on your own engineering evidence, not on the authority. A
straightforward self-built trailer in Germany goes through for around
**€430 all-in** — that figure is the floor, and it is what this becomes
*if* the brake and the arm lock are bought as certified parts and the
6 km/h rule keeps it a trailer.

## 7. Portugal — cheaper, and probably faster

Portugal runs the same EU framework (Regulamento (UE) 2018/858,
Decreto-Lei 116/2014), with **IMT** as the approval authority.
Trailers, being category O, again get **national homologation** only.

Route: technical inspection at a **CITV**, laboratory tests where
required, then the **homologação individual** dossier to IMT, then
matrícula.

| | EUR | Source |
|---|---|---|
| Homologação nacional (trailer) | 160 | published |
| Matrícula with national homologation | 45 | published |
| Matrícula without prior homologation | 165 | published |
| Simple homologation application | 45 | published |
| Individual homologation, no prior certification | 165 | published |
| CITV inspection | 30–60 | typical |
| Laboratory tests, if IMT demands them | 500–3 000 | **the open variable** |
| Engineering dossier (dossiê de fabrico) | 1 000–3 000 | as in Germany |
| **Realistic total** | **≈ 1 700 – 6 500** | |

**Stated IMT timeline: 4–12 weeks**, longer where lab testing is
required. Trailers over 300 kg must be registered.

**Portugal looks materially cheaper** — the fees are an order of
magnitude below the German engineering bill, and the process is
document-led rather than inspector-led. The risk is the mirror image:
IMT may demand accredited **laboratory testing** where a German
Sachverständiger would accept a calculation, and lab testing is where
budgets die. Ask that question first.

### The catch that decides it

**You must register where you normally live.** Germany requires a
vehicle brought in by a resident to be re-registered on German plates
within **12 months** (§ 18(2) FZV), and foreign plates are only good
while the vehicle's regular base is genuinely abroad. Portuguese plates
on a boat that lives in Germany means fines and no valid insurance —
which is the part that actually hurts.

So the Portuguese route is real **if** Max's normal residence is (or
becomes) Portugal, or the boat genuinely lives there. It is not a
shopping trip.

### And a national approval does not travel freely

Article 46 of Regulation 2018/858: *"The validity of a national
individual vehicle approval shall be restricted to the territory of the
Member State that granted it."* Another Member State **shall permit**
registration — *"unless that Member State has reasonable grounds to
believe that the relevant alternative requirements … are not equivalent
to its own"*.

In practice: a Portuguese approval is a strong argument in Germany, not
a right. German authorities can and do ask for equivalence evidence on
unusual vehicles, and this is an unusual vehicle. Budget for a partial
re-run if the boat moves country.

## 8. The boat side, in one paragraph

The Recreational Craft Directive 2013/53/EU **exempts craft built for
own use**, provided they are not placed on the EU market for **five
years** from being put into service. Sell it inside those five years
and it needs a **post-construction assessment** by a notified body
before sale — expensive and retrospective, so if there is any chance of
selling early, document the build as if it were being certified:
scantlings, stability, ISO 12217 category, CE plate data. Design
category C (coastal) or D (sheltered) allows self-certification for a
hull under 12 m, which this is.

## 9. Recommendation

1. **Cap the land drive at 6 km/h and say so on the drawings.** This is
   the single highest-value decision in the whole approval story: it
   keeps the vehicle a trailer, keeps the Sealander precedent on our
   side, and keeps us out of the amphibian dual-marking swamp.
2. **Design the running gear around a catalogue hydraulic overrun brake
   system.** The brake picks the axle geometry.
3. **Buy a pre-assessment now, before more CAD.** €300–800 at a
   technical service, in whichever country you will register. Ask for a
   written list of required evidence. Everything above is desk
   research; that letter is the real answer.
4. **Register where you live.** Portugal is cheaper on paper and worth
   pursuing *if* the boat's home is Portugal. Otherwise Germany, and
   spend the saving on engineering evidence instead.
5. **Keep a build file from the first weld** — material certificates,
   weld records, photographs, part approval sheets. It costs nothing
   during the build and is unrecoverable afterwards.

### Also worth knowing: the Netherlands

If neither country's answer is workable, the **RDW** route is the most
transparent in the EU: a self-built trailer gets an *Individueel
Goedkeuringscertificaat* at a published price list — vehicle
identification €58.50, approval assessment €72.50–110.00, IGC €72.50,
registration certificate €50.00, so **≈ €250–300 in fees** — inspected
at an RDW station, with the required certificates listed explicitly
(braking system, coupling, underrun protection). The same residency
rule applies.

## 10. Sources

- [§ 21 StVZO — Betriebserlaubnis für Einzelfahrzeuge](https://www.buzer.de/21_StVZO.htm)
- [TÜV SÜD — Vollgutachten § 21 StVZO](https://www.tuvsud.com/de-de/branchen/mobilitaet-und-automotive/import-und-zulassung/paragraph-21-gutachten)
- [Einzelabnahme 2026 — cost overview](https://www.kostenlupe.de/artikel/einzelabnahme-tuev-kosten)
- [AnhängerForum — legal requirements and real costs of a self-built trailer](https://anhaengerforum.de/forum/thread/2140-rechtliches-beim-selbstbau/)
- [§ 3 FZV — Notwendigkeit einer Zulassung (6 km/h)](https://www.gesetze-im-internet.de/fzv_2023/__3.html)
- [§ 41 StVZO — Bremsen](https://www.gesetze-im-internet.de/stvzo_2012/__41.html)
- [Regulation (EU) 2018/858 — consolidated text](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02018R0858-20240701)
- [Article 46 — validity of national individual approvals](https://www.legislation.gov.uk/eur/2018/858/article/46/adopted/data.htm?view=plain)
- [KBA — EU individual vehicle approvals](https://www.kba.de/EN/Themen_en/Typgenehmigung_en/Typgenehmigungserteilung_en/Spezielle_Genehmigungen_en/EU_Fz_Einzelgenehmigungen/eu_Fz_Einzelgenehmigungen_node.html)
- [IMT — homologação de reboques (O1–O4)](https://www.imt-ip.pt/sites/IMTT/Portugues/Veiculos/Aprovacoes/HomologacoesVeiculos/Reboques/Paginas/HomologacaoReboques.aspx)
- [Legalizar reboque caseiro — fees and documents (PT)](https://www.e-konomista.pt/legalizar-reboque-caseiro/)
- [Homologação individual no IMT — process and timeline](https://gtauto.pt/blog/homologacao-individual-imt.html)
- [RDW — self-built trailer approval and fees](https://www.rdw.nl/zakelijke-partners/fabrikant/keuren-bij-afbouw-zelfbouw-of-wijziging/aanhangwagen)
- [Sealander — caravan and category D motorboat, court ruling on amphibian status](https://www.srf.ch/news/schweiz/gerichtsurteil-zur-schifffahrt-schwimmender-wohnwagen-darf-aufs-wasser-was-das-urteil-bedeutet)
- [Recreational Craft Directive 2013/53/EU](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32013L0053)
- [Foreign plates in Germany — 12-month rule](https://www.anmeldefuchs.de/blog/auslandskennzeichen-in-deutschland)
