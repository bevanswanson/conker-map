const API_URL = '/api/conkers';

fetch(API_URL)
  .then(res => res.json())
  .then(data => {
    data.forEach(c => {
      L.marker([c.latitude, c.longitude]).addTo(map).bindPopup(c.notes);
      // console.log(c)
    });
  });

// map.on('click', e => {
//   fetch(API_URL, {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ latitude: e.latlng.lat, longitude: e.latlng.lng, notes: 'New conker!' })
//   })
//   .then(res => res.json())
//   .then(c => {
//     L.marker([c.latitude, c.longitude]).addTo(map).bindPopup(c.notes);
//   });
// });
