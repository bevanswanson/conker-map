<script lang="ts">
    import { onMount } from 'svelte';
    import L from 'leaflet';
    import 'leaflet/dist/leaflet.css';
    
    const API_URL = '/api/conkers';

    const leedsCentreCoords = [53.79822, -1.54701]
    let map;

    const conkerIcon = new L.Icon({
        iconUrl: '/conker.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    })
    
    onMount(() => {
        map = L.map('map').setView(leedsCentreCoords, 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        }).addTo(map);
        
        fetch(API_URL)
        .then(res => res.json())
        .then(data => {
            data.forEach(c => {
                L.marker([c.latitude, c.longitude], {icon: conkerIcon}).addTo(map).bindPopup(c.notes);
                console.log(c)
            });
        });
        
        
        map.on('click', e => {
            fetch(API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ latitude: e.latlng.lat, longitude: e.latlng.lng, notes: 'New conker!' })
            })
            .then(res => res.json())
            .then(c => {
                L.marker([c.latitude, c.longitude], { icon: conkerIcon })
                .addTo(map)
                .bindPopup(c.notes);
            });
        })
    });
</script>

<style>
  #map {
    height: 100vh;
    width: 100vw;
  }
</style>

<div id="map"></div>
