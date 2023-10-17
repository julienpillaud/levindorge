$(function () {

    // Search and filter table rows
    $("#search").on("keyup", function () {
        let value = $(this).val().toLowerCase();
        $("table tbody tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    // Sort table columns
    $("th:not(.not-sortable)").on("click", function () {
        let table = $(this).parents("table.sortable").eq(0)
        let rows = table.find("tr:gt(0)").toArray().sort(compare($(this).index()))
        this.asc = !this.asc
        if (!this.asc) {
            rows = rows.reverse()
        }
        for (let i = 0; i < rows.length; i++) {
            table.append(rows[i])
        }
    });

    // Color sell price
    $("table#articlesList tbody tr").each(function () {
        let $recommended_price = $("td:nth-child(9)", this);
        let recommended_price = Number($recommended_price.html());
        let $sell_price = $("td:nth-child(10)", this);
        let sell_price = Number($sell_price.html());

        if (sell_price > recommended_price) {
            $sell_price.css("background-color", "darkgreen");
        } else if (sell_price < recommended_price) {
            $sell_price.css("background-color", "darkred");
        }
    });

    // Color stock quantity
    $("table#articlesList tbody tr td:nth-child(13)").each(function () {
        let $elem = $(this);
        let value = Number($elem.html());

        if (value > 0) {
            $elem.css("background-color", "darkgreen");
        } else if (value < 0) {
            $elem.css("background-color", "darkred");
        }
    });

});

function isNumeric(value) {
    return !isNaN(parseFloat(value)) && isFinite(value);
}

function getCellValue(row, index) {
    return $(row).children("td").eq(index).text()
}

function compare(index) {
    return function (a, b) {
        let valA = getCellValue(a, index), valB = getCellValue(b, index)
        return isNumeric(valA) && isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB)
    }
}

function toggleEmptyRows() {
    let $rows = $("table tbody tr")
    let rows = document.querySelectorAll("table tbody tr")
    let noEmptyRows = Array.from(rows).filter(row => row.cells[row.cells.length - 1].children[0].value)

    if ($rows.is(":hidden")) {
        $rows.show()
    } else {
        $(rows).hide()
        $(noEmptyRows).show()
    }
}
