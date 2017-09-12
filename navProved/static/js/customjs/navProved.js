let NavProved = (() => {
	const _baseUrl = '/navProved/';

	const sendRequest = (endPoint, params, callback) => {
		$.ajax({
			url : _baseUrl + endPoint,
			data : params,
			dataType: 'json',
			type : "POST",
			success : (response) => {
				if (!response.status) {
					
				}
				else if (typeof callback === 'function') {
					callback(response);
				}
			},
			error : (error) => {
				// alert("Something went wrong....");
			},
		});
	}

	const get2DigitNumber = (val) => {
		return parseFloat(Math.round(val * 100) / 100)
	}

	const drawDataTable = (response) => {
		window.navProvedTable.rows().remove().draw();
		window.footerData = []
		let rows = response.table_data
		for (let i = 0; i < rows.length; i ++) {
			let row = [rows[i][0]]
			for (let j = 1; j < rows[i].length; j ++) {
				row.push(get2DigitNumber(rows[i][j]))
			}

			
			for (let j = 1; j < rows[i].length; j++) {
				if (!window.footerData[j]) {
					window.footerData[j] = 0
				}
				window.footerData[j] += parseFloat(rows[i][j])
			}

			window.navProvedTable.row.add(row).draw();
		}
		$("#pv").text('$ ' + get2DigitNumber(footerData[footerData.length - 1]));
		$("#pv_1").text('$ ' + get2DigitNumber(footerData[footerData.length - 1] * 6 / footerData[footerData.length - 13]));
		$("#pv_2").text('$ ' + get2DigitNumber(footerData[footerData.length - 1] / footerData[footerData.length - 13]));

		let declineRates = response.decline_rates;
		for (key in declineRates) {
			$(`input.decline-rate[data-prod-id=${key}]`).val(get2DigitNumber(declineRates[key]) + " %")
		}
	}

	const navProved = (val) => {
		sendRequest("navProvedAjax/", {"val" : val}, (response) => {
			drawDataTable(response)
		});
	}

	const init = () => {
		$(document)
		.on("click", "#sendAjaxData", (event) => {
			let dateRange = [];
			// let prod_status = 0;
			let year_status = 0;

			
			$(".date-range").each(function(){
				dateRange.push($(this).val());
			});

			for (let i = 0; i < dateRange.length; i ++) {
				if (!dateRange[i]){
					year_status = 1;
				}
			};

			if (year_status == 1){
				alert('Please fill in the year range fields...');
			}
			
			let val = JSON.stringify(dateRange);
			// let val_prod = JSON.stringify(production);
			
			if (year_status == 0){
				navProved(val);
			}
		})
		.on("change", "input.initial_production", (event) => {
			let id = event.target.getAttribute("data-id"),
				value = event.target.value;

			let dateRangeEls = document.getElementsByClassName("date-range");
			let start = dateRangeEls[0].value;
			let end = dateRangeEls[1].value;
			let drawFlag = true

			if (start == "" || end == "") {
				drawFlag = false
			}

			sendRequest('ini_prod/change/', {
				start: start,
				end: end,
				id: id,
				value: value,
				table_data_flag: drawFlag
			}, (response) => {
				drawFlag && drawDataTable(response)
			})
		})

		window.navProvedTable = $('#datatable').DataTable({
			"scrollX": true,
			"fnFooterCallback": function( nFoot, aData, iStart, iEnd, aiDisplay ) {
				let api = this.api()
				api.column(0).footer().innerHTML = "Total";
				for (let i = 1; window.footerData && i < window.footerData.length; i ++){
					api.column(i).footer().innerHTML = get2DigitNumber((window.footerData) ? window.footerData[i] : 0)
				}
			}
		});
	}

	return {
		init : init
	}
})();

((window, $) => {
		
	NavProved.init();
})(window, jQuery);