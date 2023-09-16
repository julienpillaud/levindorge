$(function() {

  // Calculate values if its a creation or an update
  if ( $('#form_product').length > 0 ) {
    calculate_taxfree_price(true);
  }

  // Calculate taxfree on buy price change
  let buyPriceArray = document.querySelectorAll("#buy_price, #excise_duty, #social_security_levy")
  buyPriceArray.forEach(function(elem) {
    elem.addEventListener("input", function() {
        console.log("calculate_taxfree_price")
        calculate_taxfree_price(false);
    });
  });

  // Calculate profit and margin on sell price change
    let sellPriceArray = document.querySelectorAll("[id^='sell_price_']")
    sellPriceArray.forEach(function(elem) {
      elem.addEventListener("input", function() {
          console.log("get_margins")
          get_margins();
      });
    });

});

//=============================================================================
function calculate_taxfree_price(on_load) {
  $.ajax({
    url: '/catalog/taxfree_price',
    type: 'POST',
    data: {
      'buy_price': $('#buy_price').val(),
      'excise_duty': $('#excise_duty').val(),
      'social_security_levy': $('#social_security_levy').val(),
    },
    success: function(json) {
      $('#taxfree_price').val(json.taxfree_price);
      calculate_recommended_prices(on_load);
    }
  });
};

function calculate_recommended_prices(on_load) {
  $.ajax({
    url: '/catalog/recommended_prices',
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
};

function get_margins() {
  var sell_prices = {};
  $('[id^="sell_price_"]').each(function() {
    sell_prices[$(this).attr('id')] = $(this).val();
  });

  $.ajax({
    url: '/catalog/margins',
    type: 'POST',
    data: {
      'taxfree_price': $('#taxfree_price').val(),
      'tax': $('#tax').val(),
      'sell_prices': JSON.stringify(sell_prices)
    },
    success: function(json) {
      $.each(json.profits, function(index, value) {
        $('#profit_' + index).val(value);
      });
      $.each(json.margins, function(index, value) {
        $('#margin_' + index).val(value);
      });
      color_sell_prices();
      enable_form_submit();
    }
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
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// Inventaire
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function inventory() {
  var sum_sale_value = 0;
  var sum_deposit_value = 0;

  $('tr').each(function() {
    var packaging = $('#packaging', this).html();
    var deposit = $('#deposit', this).html();
    var buy_price = $('#buy_price', this).html();
    var quantity = $('#quantity', this).val();
    
    if (quantity != 0) {
      var sale_value = buy_price * quantity;
      sale_value = sale_value.toFixed(2);
      $('#sale_value', this).html(sale_value);
      if (!isNaN(sale_value) && sale_value.length != 0) {
        sum_sale_value += parseFloat(sale_value);
      };
      
      if (deposit > 0) {
        var deposit_value = quantity / packaging * deposit;
        deposit_value = deposit_value.toFixed(2);
        $('#deposit_value', this).html(deposit_value);
        if (!isNaN(deposit_value) && deposit_value.length != 0) {
          sum_deposit_value += parseFloat(deposit_value);
        };
      };
    };
  });
  sum_sale_value = sum_sale_value.toFixed(2);
  $('#sum_sale_value').html(sum_sale_value);
  sum_deposit_value = sum_deposit_value.toFixed(2);
  $('#sum_deposit_value').html(sum_deposit_value);
  sum = parseFloat(sum_sale_value) + parseFloat(sum_deposit_value)
  $('#sum').html(sum);
};

$(document).ready(function() {
  $('table').keyup(inventory)
});

