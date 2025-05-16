
function afficher(id) {
    document.querySelectorAll('.viz-section').forEach(div => {
        div.style.display = 'none';
    });
    document.getElementById(id).style.display = 'block';
}

// ================= VIZ 1 : Carte des pays =================
fetch('donnees_pays_highcharts.json')
  .then(response => response.json())
  .then(data => {
    fetch('https://code.highcharts.com/mapdata/custom/world.topo.json')
      .then(res => res.json())
      .then(topology => {
        Highcharts.mapChart('container1', {
          chart: { map: topology },
          title: { text: 'Médailles olympiques par pays' },
          mapNavigation: {
            enabled: true,
            enableDoubleClickZoomTo: true,
            buttonOptions: { verticalAlign: 'bottom' }
          },
          colorAxis: {
            min: 1,
            max: Math.max(...data.map(p => p.value)),
            type: 'linear'
          },
          tooltip: {
            pointFormat: '<b>{point.name}</b><br>🥇 {point.gold} | 🥈 {point.silver} | 🥉 {point.bronze}'
          },
          series: [{
            data: data,
            joinBy: ['hc-key', 'hc-key'],
            name: 'Total médailles',
            states: { hover: { color: '#BADA55' } },
            dataLabels: { enabled: false }
          }]
        });
      });
  });

// ================= VIZ 2 : Top 10 =================
fetch('donnees_pays_medailes.json')
  .then(response => response.json())
  .then(data => {
    const top10 = data.map(entry => ({
      name: entry.pays,
      total: entry.or + entry.argent + entry.bronze
    }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 10);

    Highcharts.chart('container2', {
      chart: { type: 'column' },
      title: { text: 'Top 10 des pays les plus médaillés aux JO' },
      xAxis: {
        type: 'category',
        labels: { rotation: -45, style: { fontSize: '13px' } },
        categories: top10.map(p => p.name)
      },
      yAxis: {
        min: 0,
        title: { text: 'Total médailles' }
      },
      legend: { enabled: false },
      tooltip: {
        pointFormat: 'Total médailles : <b>{point.y}</b>'
      },
      series: [{
        name: 'Médailles',
        colorByPoint: true,
        data: top10.map(p => [p.name, p.total]),
        dataLabels: {
          enabled: true,
          rotation: -90,
          color: '#FFFFFF',
          inside: true,
          format: '{point.y}',
          y: 10,
          style: { fontSize: '13px' }
        }
      }]
    });
  });

// ================= VIZ 3 : Par sport =================
let sportsData = [];

async function chargerSports() {
  const response = await fetch('sports_medals_by_country.json');
  sportsData = await response.json();
  const select = document.getElementById("sportSelect");
  sportsData.forEach(sport => {
    const option = document.createElement("option");
    option.value = sport.discipline;
    option.textContent = sport.discipline;
    select.appendChild(option);
  });

  select.addEventListener("change", () => {
    dessinerGraphiqueParSport(select.value);
  });

  dessinerGraphiqueParSport(sportsData[0].discipline);
}

function dessinerGraphiqueParSport(discipline) {
  const sport = sportsData.find(s => s.discipline === discipline);
  if (!sport) return;

  const categories = sport.repartition.map(entry => entry.pays);
  const gold = sport.repartition.map(entry => entry.or);
  const silver = sport.repartition.map(entry => entry.argent);
  const bronze = sport.repartition.map(entry => entry.bronze);

  Highcharts.chart('container3', {
    chart: { type: 'bar' },
    title: { text: `Médailles par pays - ${discipline}` },
    xAxis: { categories },
    yAxis: {
      min: 0,
      title: { text: 'Total médailles' },
      stackLabels: { enabled: true }
    },
    legend: { reversed: true },
    tooltip: {
      formatter: function () {
        return `<b>${this.x}</b><br>${this.series.name}: ${this.y}<br>Total: ${this.point.stackTotal}`;
      }
    },
    plotOptions: {
      series: {
        stacking: 'normal',
        dataLabels: { enabled: true }
      }
    },
    series: [
      { name: '🥉 Bronze', data: bronze, color: '#cd7f32' },
      { name: '🥈 Argent', data: silver, color: '#c0c0c0' },
      { name: '🥇 Or', data: gold, color: '#ffd700' }
    ]
  });
}

chargerSports();
