$(document).ready(function () {

  const cityField = $("#city");
  const localityField = $("#locality");
  const subLocalityField = $("#sub_locality");
  const projectField = $("#project");

  function resetLocality() {
    localityField.html('<option value="">---------</option>');
  }

  function resetSubLocality() {
    subLocalityField.html('<option value="">---------</option>');
  }

  function resetProject() {
    projectField.html('<option value="">---------</option>');
  }

  cityField.on("change", function () {
    const cityId = $(this).val();

    resetLocality();
    resetSubLocality();
    resetProject();

    if (!cityId) return;

    $.ajax({
      url: "/ajax/load-localities/",
      data: { city: cityId },
      success: function (data) {
        localityField.html(data);
      }
    });
  });

  localityField.on("change", function () {
    const localityId = $(this).val();

    resetSubLocality();
    resetProject();

    if (!localityId) return;

    $.ajax({
      url: "/ajax/load-sub-localities/",
      data: { locality: localityId },
      success: function (data) {
        subLocalityField.html(data);
      }
    });

    $.ajax({
      url: "/ajax/load-projects/",
      data: { locality: localityId },
      success: function (data) {
        projectField.html(data);
      }
    });
  });

});
