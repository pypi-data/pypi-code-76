# -*- coding: utf-8 -*-
html_body = """
<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Orbis-Eval</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

    {css_color}
    {css_text_container}
    {css_dropdown}
        <style>

    .btn-secondary:focus{{
        background-color: gray;
        border-color:white;
    }}
    </style>
</head>

<body>
    <main role="main" id="main">
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-4">
                    <h1>Orbis</h1>
                </div>
                <div class="col-md-8">
                    <div class="switch-container">
                      <div class="switch-description">Click to toggle dark mode</div>
                      <label class="switch">
                        <input type="checkbox" onclick="darkLight()" id="checkBox" >
                        <span class="slider"></span>
                      </label>
                    </div>
                </div>
            </div>
            {orbis_header}
            {item_header}
        </div>

        <div class="container-fluid">
            {navigation}
            <!-- Example row of columns -->

            <div class="row" id="text-container">
                {gold_corpus}
                {predicted_corpus}
            </div>
            <button onclick="showMore()" class="btn btn-secondary show-more-button" type="button">Show More</button>

            <div class="row">
                {gold_entities}
                {predicted_entities}
            </div>

        </div>
    </main>
<script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script type="text/javascript" src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

{js_arrow_key_navigation}
{js_color}
{js_navigation}
{js_dropdown}

</body>

</html>
"""
