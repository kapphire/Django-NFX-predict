let NavProved = (() => {
	const _baseUrl = '/';

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
					callback(response.table_data);
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

	const navProved = (val) => {
		sendRequest("navProved/navProvedAjax/", {"val" : val}, (results) => {
			window.navProvedTable.rows().remove().draw();

			window.footerData = []
			for (let i = 0; i < results.length; i ++) {
				let row = [results[i][0]]
				for (let j = 1; j < results[i].length; j ++) {
					row.push(get2DigitNumber(results[i][j]))
				}

				
				for (let j = 1; j < results[i].length; j++) {
					if (!window.footerData[j]) {
						window.footerData[j] = 0
					}
					window.footerData[j] += parseFloat(results[i][j])
				}

				window.navProvedTable.row.add(row).draw();
			}
			$("#pv").text('$ ' + get2DigitNumber(footerData[footerData.length - 1]));
			$("#pv_1").text('$ ' + get2DigitNumber(footerData[footerData.length - 1] * 6 / footerData[footerData.length - 13]));
			$("#pv_2").text('$ ' + get2DigitNumber(footerData[footerData.length - 1] / footerData[footerData.length - 13]));
		});
	}

	const init = () => {
		$(document)
		.on("click", "#sendAjaxData", (event) => {
			let declineRate = [];
			let dateRange = [];
			let valArr = [];
			
			$(".date-range").each(function(){
				dateRange.push($(this).val());
			});

			let val = JSON.stringify(dateRange);
			
			navProved(val);
		})

		window.navProvedTable = $('#datatable').DataTable({
			"scrollY": 400,
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