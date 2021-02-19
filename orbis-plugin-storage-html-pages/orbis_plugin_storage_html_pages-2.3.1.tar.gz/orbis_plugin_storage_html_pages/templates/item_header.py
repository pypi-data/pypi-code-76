item_header = """
<div class="row">

    <div class="col-md-9">
        <h2>
        Stats for Item {item_number}
        </h2>
    </div>
    <div class="col-md-3">

        <div class="btn-group color-mode-container" role="group" aria-label="Color Modes">
            <button id="entities_button" class="btn btn-secondary active" type="button">Entities</button>
            <button id="types_button" class="btn btn-secondary" type="button">Types</button>
            {display_buttons}
            <button id="results_button" class="btn btn-secondary" type="button">Results</button>
        </div>

    </div>

    <div class="col-md-6">
        <p>{item_column_0}</p>
    </div>
    <div class="col-md-6">
        <p>{item_column_1}</p>
    </div>
</div>
"""
