django.jQuery(document).ready(function($) {
    
    var cityField = $('#id_city');
    var localityField = $('#id_locality');
    var subLocalityField = $('#id_sub_locality');
    var projectField = $('#id_project');

    // --- Logic: Dropdown ko Reset aur Disable karne ka ---
    function disableDropdown(field) {
        field.html('<option value="">---------</option>');
        field.prop('disabled', true); // LOCK kar diya
        field.css('background-color', '#e9ecef'); // Grey color
        field.css('cursor', 'not-allowed');
    }

    function enableDropdown(field) {
        field.prop('disabled', false); // UNLOCK kar diya
        field.css('background-color', '#ffffff'); // White color
        field.css('cursor', 'default');
    }

    // --- Page Load Logic ---
    // Agar City khali hai, to Locality, SubLocality, Project sab LOCK rahenge
    if (!cityField.val()) {
        disableDropdown(localityField);
        disableDropdown(subLocalityField);
        disableDropdown(projectField);
    } 
    // Agar Locality khali hai, to uske neeche wale LOCK rahenge
    else if (!localityField.val()) {
        disableDropdown(subLocalityField);
        disableDropdown(projectField);
    }

    // --- EVENT 1: City Change Logic ---
    cityField.change(function() {
        var url = "/ajax/load-localities/";  
        var cityId = $(this).val();

        // City badalte hi niche wale sab LOCK
        disableDropdown(localityField);
        disableDropdown(subLocalityField);
        disableDropdown(projectField);

        if (cityId) {
            $.ajax({
                url: url,
                data: { 'city': cityId },
                success: function(data) {
                    localityField.html(data);
                    enableDropdown(localityField); // Data aane par UNLOCK
                }
            });
        }
    });

    // --- EVENT 2: Locality Change Logic ---
    localityField.change(function() {
        var url = "/ajax/load-sub-localities/";
        var localityId = $(this).val();

        disableDropdown(subLocalityField);
        disableDropdown(projectField);

        if (localityId) {
            $.ajax({
                url: url,
                data: { 'locality': localityId },
                success: function(data) {
                    subLocalityField.html(data);
                    enableDropdown(subLocalityField); // Data aane par UNLOCK
                    enableDropdown(projectField); // Project bhi UNLOCK
                }
            });
        }
    });
});