let NavTotal = (() => {
	const _baseUrl = '/navTotal/';

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

	// const drawDataTable = (response) => {
	// 	window.navProvedTable.rows().remove().draw();
	// 	window.footerData = []
	// 	let rows = response.table_data
	// 	for (let i = 0; i < rows.length; i ++) {
	// 		let row = [rows[i][0]]
	// 		for (let j = 1; j < rows[i].length; j ++) {
	// 			row.push(get2DigitNumber(rows[i][j]))
	// 		}

			
	// 		for (let j = 1; j < rows[i].length; j++) {
	// 			if (!window.footerData[j]) {
	// 				window.footerData[j] = 0
	// 			}
	// 			window.footerData[j] += parseFloat(rows[i][j])
	// 		}

	// 		window.navProvedTable.row.add(row).draw();
	// 	}
	// 	$("#pv").text('$ ' + get2DigitNumber(footerData[footerData.length - 1]));
	// 	$("#pv_1").text('$ ' + get2DigitNumber(footerData[footerData.length - 1] * 6 / footerData[footerData.length - 13]));
	// 	$("#pv_2").text('$ ' + get2DigitNumber(footerData[footerData.length - 1] / footerData[footerData.length - 13]));

	// 	let declineRates = response.decline_rates;
	// 	for (key in declineRates) {
	// 		$(`input.decline-rate[data-prod-id=${key}]`).val(get2DigitNumber(declineRates[key]) + " %")
	// 	}
	// }

	const navTotal = (acre_unconv, risk_unconv, spacing, zone, zone_pros, rigs, days_to, drilled) => {
		sendRequest("navTotalAjax/",
		{
			"acre_unconv" : acre_unconv, 
			"risk_unconv" : risk_unconv,
			"spacing" : spacing,
			"zone" : zone,
			"zone_pros" :zone_pros,
			"rigs" : rigs,
			"days_to" : days_to,
			"drilled" : drilled
		}, (response) => {
			console.log("success")
		});
	}

	const navTotalInitVariables = (total_net_asset_value, total_inflation, total_rig, total_m_a, total_ngl_percent, total_duration, total_year_define, total_boe_mcfe) => {
		sendRequest("navTotalInitVariables/",
		{
			"total_net_asset_value" : total_net_asset_value, 
			"total_inflation" : total_inflation,
			"total_rig" : total_rig,
			"total_m_a" : total_m_a,
			"total_ngl_percent" : total_ngl_percent, 
			"total_duration" : total_duration, 
			"total_year_define" : total_year_define, 
			"total_boe_mcfe" : total_boe_mcfe
		}, (response) => {
			alert("Successfully changed...")
		});
	}

	const init = () => {
		total_m_a_val = 1 - $("#total-rig").val();
		$("#total-m-a").val(total_m_a_val);

		$(document)
		.on("change", "#total-rig", (event) => {
			total_m_a_val = 1 - $("#total-rig").val();
			$("#total-m-a").val(total_m_a_val);
		})

		.on("click", "#confirm-total-variable", (event) => {
			$('.total-variables').each(function (i, obj) {
				if ($(this).val() == "") {
					alert("Please fill in all variables...");
					return false;
				}
			});

			let total_net_asset_value = $("#total-net-asset-value").val(),
				total_inflation = $("#total-inflation").val(),
				total_rig = $("#total-rig").val(),
				total_m_a = $("#total-m-a").val(),
				total_ngl_percent = $("#total-ngl-percent").val(),
				total_duration = $("#total-duration").val(),
				total_year_define = $("#total-year-define").val(),
				total_boe_mcfe = $("#total-boe-mcfe").val();

			console.log(total_year_define)

			navTotalInitVariables(total_net_asset_value, total_inflation, total_rig, total_m_a, total_ngl_percent, total_duration, total_year_define, total_boe_mcfe)
				
		})

		.on("click", "#unconventional-toggle", (event) => {
			unconventional_state = $("#unconventional-toggle").attr("class");
			if (unconventional_state == 'btn') {
				$('#unconventional').css('display', '');
			}else{
				$('#unconventional').css('display', 'none');
			};
		})

		.on("click", "#conventional-toggle", (event) => {
			conventional_state = $("#conventional-toggle").attr("class");
			if (conventional_state == 'btn') {
				$('#conventional').css('display', '');
			}else{
				$('#conventional').css('display', 'none');
			};
		})


		.on("click", "#unconventional-view", (event) => {
			let acre_unconv = $("#acre-unconv").val();
			let risk_unconv = $("#risk-unconv").val();
			let spacing = $("#spacing").val();
			let zone = $("#zone").val();
			let zone_pros = $("#zone-pros").val();
			let rigs = $("#rigs").val();
			let days_to = $("#days-to").val();
			let drilled = $("#drilled").val();
			
			if (acre_unconv == "" || risk_unconv == "" || spacing == "" || zone == "" || zone_pros == "" || rigs == "" || days_to == "" || drilled == "") {
				alert("please fill in the all inputs.")
			}

			navTotal(acre_unconv, risk_unconv, spacing, zone, zone_pros, rigs, days_to, drilled);
		})
		// .on("change", "input.initial_production", (event) => {
		// 	let id = event.target.getAttribute("data-id"),
		// 		value = event.target.value;

		// 	let dateRangeEls = document.getElementsByClassName("date-range");
		// 	let start = dateRangeEls[0].value;
		// 	let end = dateRangeEls[1].value;
		// 	let drawFlag = true

		// 	if (start == "" || end == "") {
		// 		drawFlag = false
		// 	}

		// 	sendRequest('ini_prod/change/', {
		// 		start: start,
		// 		end: end,
		// 		id: id,
		// 		value: value,
		// 		table_data_flag: drawFlag
		// 	}, (response) => {
		// 		drawFlag && drawDataTable(response)
		// 	})
		// })

		window.provedReserve = $('#proved-reserves').DataTable({
			"scrollX": true,
			"paging": false,
			// "info": false,
			"searching": false,
			// "fnFooterCallback": function( nFoot, aData, iStart, iEnd, aiDisplay ) {
			// 	let api = this.api()
			// 	api.column(0).footer().innerHTML = "Total";
			// 	for (let i = 1; window.footerData && i < window.footerData.length; i ++){
			// 		api.column(i).footer().innerHTML = get2DigitNumber((window.footerData) ? window.footerData[i] : 0)
			// 	}
			// }
		});

		window.addPlayUnconventional = $("#add-play-unconventional").DataTable({
			"scrollX": true,
			"paging" : false,
			"searching" : false,
			"info" : false,
		})

		window.addPlayConventional = $("#add-play-conventional").DataTable({
			"scrollX": true,
			"paging" : false,
			"searching" : false,			
			"info" : false,
		})

		window.totalUnprovenPotential = $("#total-unproven-potential").DataTable({
			"scrollX": true,
			"paging" : false,
			"searching" : false,			
			"info" : false,
		})


	}

	return {
		init : init
	}
})();

((window, $) => {
		
	NavTotal.init();
})(window, jQuery);