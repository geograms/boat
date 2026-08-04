OPENSCAD := openscad
MODES := road launch harbor cruise foiling
SIZE := 1600,1000

# gimbal rotations per view (vpr); --viewall/--autocenter set pan+zoom
CAM_iso   := 0,0,0,65,0,35,15000
CAM_side  := 0,0,0,90,0,0,15000
CAM_front := 0,0,0,90,0,90,15000
CAM_top   := 0,0,0,0,0,0,15000

.PHONY: all check png anim stl clean

all: check png

export:
	mkdir -p export

check: export
	$(OPENSCAD) -o export/check.echo assembly.scad 2>&1 | grep -Ei 'assert|error|warning' || true
	@cat export/check.echo | grep -v WARNING

png: export
	for m in $(MODES); do \
	  for v in iso side front; do \
	    cam=$$( [ $$v = iso ] && echo "$(CAM_iso)" || ( [ $$v = side ] && echo "$(CAM_side)" || echo "$(CAM_front)" ) ); \
	    $(OPENSCAD) -o export/$${m}_$${v}.png -D "mode=\"$$m\"" \
	      --imgsize=$(SIZE) --camera=$$cam --autocenter --viewall \
	      --preview --colorscheme=Tomorrow assembly.scad; \
	  done; \
	done
	$(OPENSCAD) -o export/anchor_iso.png -D 'mode="cruise"' -D canopy_up=true \
	  --imgsize=$(SIZE) --camera=$(CAM_iso) --autocenter --viewall \
	  --preview --colorscheme=Tomorrow assembly.scad

anim: export
	$(OPENSCAD) -o export/anim.png -D anim=true -D 'mode="cruise"' \
	  --imgsize=800,600 --camera=$(CAM_front) --autocenter --viewall \
	  --animate 36 --preview --colorscheme=Tomorrow assembly.scad
	@echo "frames in export/anim*.png — e.g. ffmpeg -i export/anim%05d.png unfold.gif"

stl: export
	$(OPENSCAD) -o export/boat_1to20_cruise.stl -D 'mode="cruise"' -D 'target="print"' assembly.scad
	$(OPENSCAD) -o export/boat_1to20_road.stl   -D 'mode="road"'   -D 'target="print"' assembly.scad

clean:
	rm -rf export
