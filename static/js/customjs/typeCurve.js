let TypeCurves = (() => {
	const _baseUrl = '/typeCurve/';

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
				alert("Something went wrong....");
			},
		});
	}

	const get2DigitNumber = (val) => {
		return parseFloat(Math.round(val * 100) / 100)
	}

	const drawDataTable = (response) => {
		window.typeCurveTable.rows().remove().draw();
		window.footerData = []
		let rows = response.result
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

			window.typeCurveTable.row.add(row).draw();
		}

		// $("#pv").text('$ ' + get2DigitNumber(footerData[footerData.length - 1]));
		// $("#pv_1").text('$ ' + get2DigitNumber(footerData[footerData.length - 1] * 6 / footerData[footerData.length - 13]));
		// $("#pv_2").text('$ ' + get2DigitNumber(footerData[footerData.length - 1] / footerData[footerData.length - 13]));

		let declineRates = response.decline_rates;
		for (key in declineRates) {
			$(`td.decline-value[data-id=${key}]`).text(get2DigitNumber(declineRates[key]) + " %")
		}
	}

	const typeCurve = (val) => {
		sendRequest("typeCurveAjax/", {"val" : val}, (response) => {
			drawDataTable(response)
		});
	}

	const init = () => {
		$(document)
		.on("click", "#typeCurveAjax", (event) => {
			
			let val = $("#type_curve_year").val()
			if (val != '') {
				typeCurve(val)
			}
			else{
				alert("Please fill in the year input box...")
			}

		})
		.on("change", "input.common-input", (event) => {
			let id = event.target.getAttribute("data-id"),
				value = event.target.value;

			let dateRangeEl = document.getElementById("type_curve_year");
			let start = dateRangeEl.value;
			let drawFlag = true

			if (start == "") {
				drawFlag = false
			}

			sendRequest('ini_prod/change/', {
				start: start,
				id: id,
				value: value,
				table_data_flag: drawFlag
			}, (response) => {
				drawFlag && drawDataTable(response)
			})
		})

		window.typeCurveTable = $('#typeCurve-datatable').DataTable({
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
		
	TypeCurves.init();
})(window, jQuery);