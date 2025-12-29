(function ($) {
  $(document).ready(function () {

    const cityField = $("#id_city");
    const localityField = $("#id_locality");
    const subLocalityField = $("#id_sub_locality");
    const projectField = $("#id_project");

    // --- Reset helpers ---
    function resetLocality() {
      localityField.html('<option value="">---------</option>');
    }
    function resetSubLocality() {
      subLocalityField.html('<option value="">---------</option>');
    }
    function resetProject() {
      projectField.html('<option value="">---------</option>');
    }

    // -----------------------------
    // CITY → LOCALITY
    // -----------------------------
    cityField.change(function () {
      const cityId = $(this).val();

      resetLocality();
      resetSubLocality();
      resetProject();

      if (!cityId) return;

      $.ajax({
        url: "/business/ajax/load-localities/",
        data: { city: cityId },
        success: function (data) {
          localityField.html(data);
        }
      });
    });

    // -----------------------------
    // LOCALITY → SUB LOCALITY + PROJECT
    // -----------------------------
    localityField.change(function () {
      const localityId = $(this).val();

      resetSubLocality();
      resetProject();

      if (!localityId) return;

      // Sub Locality
      $.ajax({
        url: "/business/ajax/load-sub-localities/",
        data: { locality: localityId },
        success: function (data) {
          subLocalityField.html(data);
        }
      });

      // Project
      $.ajax({
        url: "/business/ajax/load-projects/",
        data: { locality: localityId },
        success: function (data) {
          projectField.html(data);
        }
      });
    });

    // -----------------------------
    // EDIT MODE (Auto load)
    // -----------------------------
    if (cityField.val()) {
      cityField.trigger("change");
    }

    if (localityField.val()) {
      localityField.trigger("change");
    }

  });
})(django.jQuery);
