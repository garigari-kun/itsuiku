


$( "#datepicker" ).datepicker({
    dateFormat: 'yy-mm-dd',
    onSelect: function(date) {
      // alert(date);
      // form id like #id_form-TOTAL_FORMS
      var formId = "id_form-TOTAL_FORMS"
      // copy empty form
      var emptyRow = $("#empty-form").clone();
      // remove id from new form
      emptyRow.attr("id", null)
      // Insert row after last row
      // get starting form count for formset
      var totalForms = parseInt($('#' + formId).val());
      // create new form row from empty form row
      var newFormRow;
      emptyRow.find("input, select, textarea").each(function(){
          newFormRow = updateEmptyFormIDs($(this), totalForms, date)
      })


      // insert new form at the end of the last form row
      $(".form-row:last").after(newFormRow)
      // update total form count (to include new row)
      $('#'+ formId).val(totalForms + 1);

    }
 });

function updateEmptyFormIDs(element, totalForms, date){
 console.log(element);
  var thisInput = element
  // get current form input name
  var currentName = element.attr('name')
  console.log(currentName);
  // replace "prefix" with actual number
  var newName = currentName.replace(/__prefix__/g, totalForms)
  // console.log(newName)
  // update input with new name
  thisInput.attr('name', newName)
  thisInput.attr('id', "id_" + newName)
  if (currentName.indexOf('date') > 0) {
    console.log('yeah');
    thisInput.attr('value', date);

  }
  // create a new form row id
  var newFormRow = element.closest(".form-row");
  var newRowId =  "row_id_" + newName
  newFormRow.attr("id", newRowId)
  // add new class for basic graphic animation
  newFormRow.addClass("new-parent-row")
  // update form group id
  var parentDiv = element.parent();
  parentDiv.attr("id", "parent_id_" + newName)
  // update label id
  var inputLabel = parentDiv.find("label")
  inputLabel.attr("for", "id_" + newName)

  // return created row
  return newFormRow
}
