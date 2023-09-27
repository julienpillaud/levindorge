$(function() {

  // Calculate values if its a creation or an update
  if ( $('#form_product').length > 0 ) {
    calculate_taxfree_price(true);
  }

  // Calculate taxfree on buy price change
  let buyPriceArray = document.querySelectorAll("#buy_price, #excise_duty, #social_security_levy")
  buyPriceArray.forEach(function(elem) {
    elem.addEventListener("input", function() {
        calculate_taxfree_price(false);
    });
  });

  // Calculate profit and margin on sell price change
    let sellPriceArray = document.querySelectorAll("[id^='sell_price_']")
    sellPriceArray.forEach(function(elem) {
      elem.addEventListener("input", function() {
          get_margins();
      });
    });

  let quantityArray = document.querySelectorAll("#inventory tbody tr td input[name='quantity']");
  quantityArray.forEach(function(elem) {
    elem.addEventListener("input", function() {
      save_inventory(elem);
    });
  });

});

//=============================================================================
function save_inventory(elem) {
  let row = elem.closest("tr")
  let sale_value = row.querySelector("#sale_value")
  let deposit_value = row.querySelector("#deposit_value")

  let options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "articleId": row.id,
      "stockQuantity": Number(elem.value),
    }),
  }
  fetch("/inventory/save", options)
    .then(response => response.json())
    .then(body => {
      sale_value.innerHTML = body["sale_value"];
      deposit_value.innerHTML = body["deposit_value"]
    });
}

function calculate_taxfree_price(on_load) {
  const buy_price = document.getElementById("buy_price");
  const buy_price_value = buy_price ? buy_price.value : 0;

  const excise_duty = document.getElementById("excise_duty");
  const excise_duty_value = excise_duty ? excise_duty.value : 0;

  const social_security_levy = document.getElementById("social_security_levy");
  const social_security_levy_value = social_security_levy ? social_security_levy.value : 0;

  const taxfree_price = document.getElementById("taxfree_price");
  const value = Number(buy_price_value) + Number(excise_duty_value) + Number(social_security_levy_value);
  taxfree_price.value = Math.round(value * 100) / 100;

  calculate_recommended_prices(on_load);
}

function calculate_recommended_prices(on_load) {
  $.ajax({
    url: '/articles/recommended_prices',
    type: 'POST',
    data: {
      'ratio_category': $('#ratio_category').val(),
      'taxfree_price': $('#taxfree_price').val(),
      'tax': $('#tax').val()
    },
    success: function(json) {
      $.each(json, function(index, value) {
        $('#recommended_price_' + index).val(value);
        if (!on_load) {
          $('#sell_price_' + index).val(value);
        }
      });
      get_margins();
    }
  });
}

function get_margins() {
  $('[id^="sell_price_"]').each(function() {
    const sell_price = $(this).val();
    const shop = $(this).attr("id").split("sell_price_")[1];

    $.ajax({
      url: "/articles/margins",
      type: "POST",
      data: {
        "taxfree_price": $('#taxfree_price').val(),
        "tax": $('#tax').val(),
        "sell_price": sell_price,
      },
      success: function(json) {
        $('#profit_' + shop).val(json.margin);
        $('#margin_' + shop).val(json.markup);
        color_sell_prices();
        enable_form_submit();
      }
    })

  });
}

function color_sell_prices() {
  $('[id^="sell_price_"]').each(function() {
    var sell_price = parseFloat($(this).val());
    var shop = $(this).attr('id').split('sell_price_')[1];
    var recommended_price = parseFloat($('#recommended_price_' + shop).val());
    var margin = parseFloat($('#margin_' + shop).val())

    if (margin < 5) {
      $(this).css('background-color', 'indianred');
    }
    else {
      if (sell_price < recommended_price) {
        $(this).css('background-color', 'lightcoral');
      }
      else if (sell_price > recommended_price) {
         $(this).css('background-color', 'lightgreen');
      }
      else {
        $(this).css('background-color', '');
      }
    }
  });
}

function enable_form_submit() {
  // Create a list of all margins
  var margins = [];
  $('[id^="margin_"]').each(function() {
    margins.push(parseFloat($(this).val()));
  });

  // Enable create and update button only if all margins > 5%
  if (margins.some(x => x < 5)) {
    $('#create').prop('disabled', true);
    $('#update').prop('disabled', true);
  }
  else {
    $('#create').prop('disabled', false);
    $('#update').prop('disabled', false);
  }
}


// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// TRI TABLEAU
// https://stackoverflow.com/questions/3160277/jquery-table-sort
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$('th').click(function() {
    var table = $(this).parents('table').eq(0)
    var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index()))
    this.asc = !this.asc
    if (!this.asc){rows = rows.reverse()}
    for (var i = 0; i < rows.length; i++){table.append(rows[i])}
})
function comparer(index) {
    return function(a, b) {
        var valA = getCellValue(a, index), valB = getCellValue(b, index)
        return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB)
    }
}
function getCellValue(row, index){ return $(row).children('td').eq(index).text() }

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// RECHERCHE TABLEAU
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$(document).ready(function() {
  $('#search').keyup(function(){
   // Search Text
   var search = $(this).val();
   // Hide all table tbody rows
   $('table tbody tr').hide();
  // Searching text in columns and show match row
  $('table tbody tr td:contains("'+search+'")').each(function(){
   $(this).closest('tr').show();
  });
 });
});
// Case-insensitive searching (Note - remove the below script for Case sensitive search )
$.expr[":"].contains = $.expr.createPseudo(function(arg) {
 return function( elem ) {
  return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
 };
});
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// COLORATION DU PRIX TTC EN FONCTION DU PVC
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$(document).ready(function() {
  $('#article_list tr').each(function() {

    var recommended_price = Number($(this).find('.recommended_price').html());
    var sell_price = Number($(this).find('.sell_price').html());
    if (sell_price < recommended_price) {
      $(this).find('.sell_price').css('background-color', 'darkred');
    } else if (sell_price > recommended_price) {
      $(this).find('.sell_price').css('background-color', 'darkgreen');
    }

    var stock_quantity = Number($(this).find('.stock_quantity').html());
    if (stock_quantity < 0) {
      $(this).find('.stock_quantity').css('background-color', 'darkred');
    } else if (stock_quantity > 0) {
      $(this).find('.stock_quantity').css('background-color', 'darkgreen');
    }

  })
})
