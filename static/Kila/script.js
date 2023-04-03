document.addEventListener('DOMContentLoaded', function() {
  if (document.querySelector("#week-select")) {
  week_chart();
  documents()
  draw_monthly_chart();
  }
    if(document.querySelector("#search")) 
    {
    document.querySelector("#search").addEventListener("input", ()=>search(document.querySelector("#search").value))
    }
});
function documents(){
  fetch(get_obra_documentos_url())
        .then(response => response.json())
        .then(weeks => {
          weeks.forEach(week=>{
            content=`<div>${week.semana}</div>`
            let campo="<div>"
            let conformidad="<div>"
            let otros="<div>"
            week.documentos.forEach(doc=>{
              let doc_type= `
              <a href="${doc.url}" download>
                <i id="accepted-icon" class="icon-file-text" style='color:green;float: left; font-size:60px; margin:10px'></i>
                <h6 style="display:inline-block; width:100%;zzz float:left">${doc.filename}</h6>
              </a>`
              if(doc.tipo_de_documento == "Acta de Campo"){
                campo+=doc_type
              }
              else if(doc.tipo_de_documento == "Acta de Conformidad"){
                conformidad+=doc_type
              }
              else if(doc.tipo_de_documento == "Otros"){
                otros+=doc_type
              }
            })
              campo+="</div>"
              conformidad+="</div>"
              otros+="</div>"
              document.querySelector("#documents").innerHTML+=`${content}${campo}${conformidad}${otros}`;
          })
        })
}
function search(value) {
  let notes = document.querySelectorAll(".card")
  notes.forEach(function(div){
    let f = div.innerHTML.toLowerCase();
    let finded = f.search(value.toLowerCase())
    if(finded=="-1"){
      div.parentElement.style.display="none";
    }
    else{
      div.parentElement.style.display="block";
    }
  })
}
function week_chart(){
    var values=document.querySelector("#week-select").value.split("-")
    
    fetch(get_report_url()+`?type=${values[0]}&type_id=${values[1]}`)
        .then(response => response.json())
        .then(week => {
          google.charts.load('current', {'packages':['corechart']});
          google.charts.setOnLoadCallback(drawChart);
            function drawChart() {
              var data = new google.visualization.DataTable();
              data.addColumn('string', 'Indicador');
              data.addColumn('number', 'Valor');
              week.indicadores.forEach(indicador => {
                data.addRows([[indicador.indicador.nombre, indicador.valor*1]]);
              });
      
              var options = {
                title : `Semana ${week.num_semana} - Cumplimiento General ${week.cumplimiento_general}`,
                vAxis: {title: 'Valores'},
                seriesType: 'bars',
              };
      
              // Instantiate and draw our chart, passing in some options.
              var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
              chart.draw(data, options);
            }
        });
}

function draw_monthly_chart(){
    google.charts.load('current', {'packages':['line']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Mes');
      data.addColumn('number', '');
      var months_names = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
      fetch(get_report_url()+`?type=month&type_id=1`)
      .then(response => response.json())
      .then(months => {
        for (const [key, value] of Object.entries(months)) {
          data.addRows([[months_names[key], value*1]]);
        }
      })
      var height = document.body.clientHeight;
      var width = document.querySelectorAll(".container")[0].offsetWidth;
      var options = {
        chart: {
          title: 'Indice de Cumplimiento General por Mes (%)',
        },
        width: width,
        height: 500
      };

      var chart = new google.charts.Line(document.getElementById('line_monthly'));

      chart.draw(data, google.charts.Line.convertOptions(options));
    }
}