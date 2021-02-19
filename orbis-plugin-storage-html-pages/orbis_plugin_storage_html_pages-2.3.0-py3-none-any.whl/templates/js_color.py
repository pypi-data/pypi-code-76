js_color = """
<script type="text/javascript">

function removeClasses() {{
  $('.color').removeClass('entities');
  $('.color').removeClass('results');
  $('.color').removeClass('types');
  $('#entities_button').removeClass('active');
  $('#results_button').removeClass('active');
  $('#types_button').removeClass('active');
  {0}
}}

document.getElementById("types_button").onclick = function() {{

      removeClasses()
      $('.color').addClass('types');
      $('#types_button').addClass('active')
    }}

document.getElementById("entities_button").onclick = function() {{
      removeClasses()
      $('.color').addClass('entities');
      $('#entities_button').addClass('active')
    }}

document.getElementById("results_button").onclick = function() {{
      removeClasses()
      $('.color').addClass('results');
      $('#results_button').addClass('active')
    }}
    
{1}


$('#main').toggleClass(localStorage.toggled);

function darkLight() {{
  /*DARK CLASS*/
  if (localStorage.toggled != 'dark-mode') {{
    $('#main').toggleClass('dark-mode', true);
    localStorage.toggled = "dark-mode";

  }} else {{
    $('#main').toggleClass('dark-mode', false);
    localStorage.toggled = "";
  }}
}}

/*Add 'checked' property to input if background == dark-mode*/
if ($('main').hasClass('dark-mode')) {{
   $( '#checkBox' ).prop( "checked", true )
}} else {{
  $( '#checkBox' ).prop( "checked", false )
}}

</script>
"""
