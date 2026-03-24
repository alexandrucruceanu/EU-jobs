const fs = require('fs');
const d3 = require('d3-geo');
const topojson = require('topojson-client');

async function main() {
  const res = await fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-50m.json');
  const world = await res.json();
  const countries = topojson.feature(world, world.objects.countries).features;

  const euAlpha2 = {
    at: "Austria", be: "Belgium", bg: "Bulgaria", cy: "Cyprus", cz: "Czechia",
    de: "Germany", dk: "Denmark", ee: "Estonia", el: "Greece", es: "Spain",
    fi: "Finland", fr: "France", hr: "Croatia", hu: "Hungary", ie: "Ireland",
    it: "Italy", lt: "Lithuania", lu: "Luxembourg", lv: "Latvia", mt: "Malta",
    nl: "Netherlands", pl: "Poland", pt: "Portugal", ro: "Romania", se: "Sweden",
    si: "Slovenia", sk: "Slovakia"
  };

  const contextAlpha2 = {
    no: "Norway", ch: "Switzerland", gb: "United Kingdom", by: "Belarus", ua: "Ukraine", md: "Moldova", tr: "Turkey", al: "Albania", rs: "Serbia", me: "Montenegro", ba: "Bosnia and Herzegovina", mk: "North Macedonia", is: "Iceland"
  };

  const nameToId = {};
  for (const [code, name] of Object.entries(euAlpha2)) nameToId[name] = code;
  for (const [code, name] of Object.entries(contextAlpha2)) nameToId[name] = code;

  // Filter polygons that are way outside Europe (e.g. French Guiana, Reunion, Canary Islands, Greenland)
  // Europe bounding box roughly: lon -30 to 45, lat 30 to 75
  function filterPolygons(geometry) {
    if (!geometry) return geometry;
    const isInsideEurope = (ring) => {
      // average lon/lat of the ring
      let sumLon = 0, sumLat = 0;
      for (const [lon, lat] of ring) {
        sumLon += lon;
        sumLat += lat;
      }
      const avgLon = sumLon / ring.length;
      const avgLat = sumLat / ring.length;
      return (avgLon >= -35 && avgLon <= 45 && avgLat >= 27 && avgLat <= 75);
    };

    if (geometry.type === 'Polygon') {
      return isInsideEurope(geometry.coordinates[0]) ? geometry : null;
    } else if (geometry.type === 'MultiPolygon') {
      const newCoords = geometry.coordinates.filter(polygon => isInsideEurope(polygon[0]));
      if (newCoords.length === 0) return null;
      if (newCoords.length === 1) return { type: 'Polygon', coordinates: newCoords[0] };
      return { type: 'MultiPolygon', coordinates: newCoords };
    }
    return geometry;
  }

  const cleanCountries = countries.map(c => {
    return {
      ...c,
      geometry: filterPolygons(c.geometry)
    };
  }).filter(c => c.geometry != null);

  const euFeatures = cleanCountries.filter(c => euAlpha2[nameToId[c.properties.name]]);

  const projection = d3.geoConicConformal()
    .parallels([35, 65])
    .rotate([-15, 0])
    .fitSize([800, 700], {
      type: "FeatureCollection",
      features: euFeatures
    });

  const path = d3.geoPath().projection(projection);

  const out = { eu: {}, context: {}, width: 800, height: 700 };

  for (const c of cleanCountries) {
    const name = c.properties.name;
    const code = nameToId[name];
    if (!code) continue;

    const svgPath = path(c);
    if (!svgPath) continue;

    const rounded = svgPath.replace(/(\.\d)\d+/g, '$1'); 

    if (euAlpha2[code]) {
      out.eu[code] = rounded;
    } else {
      out.context[code] = rounded;
    }
  }

  fs.writeFileSync('site/eu_map_paths.json', JSON.stringify(out));
  console.log('Wrote new eu_map_paths.json without ultramar territories');
}

main().catch(console.error);
