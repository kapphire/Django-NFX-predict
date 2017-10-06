let NavTotal = (() => {
	const _baseUrl = '/navTotal/';

	const sendRequest = (endPoint, params, callback) => {
		$.ajax({
			url : _baseUrl + endPoint,
			data : params,
			dataType: 'json',
			// contentType: 'application/json',
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

	const navTotalInitVariables = (total_net_asset_value, total_inflation, total_rig, total_duration, total_year_define, total_boe_mcfe, date) => {
		sendRequest("navTotalInitVariables/",
		{
			"total_net_asset_value" : total_net_asset_value, 
			"total_inflation" : total_inflation,
			"total_rig" : total_rig,
			"total_duration" : total_duration, 
			"total_year_define" : total_year_define, 
			"total_boe_mcfe" : total_boe_mcfe,
			"date" : date,
		}, (response) => {
			alert("Successfully changed...")
		});
	}

	const navTotalEquityOffering = (equity_choice, equity_share_amount, equity_shoe, equity_last_price, equity_gross_issue, equity_net_issue, date) => {
		sendRequest("navTotalEquityOffering/", 
		{
			"equity_choice" : equity_choice, 
			"equity_share_amount" : equity_share_amount, 
			"equity_shoe" : equity_shoe, 
			"equity_last_price" : equity_last_price, 
			"equity_gross_issue" : equity_gross_issue, 
			"equity_net_issue" : equity_net_issue,
			"date" : date,
		}, (response) => {
			$('#equity-shoe-calc').html(get2DigitNumber(response.tbl_dict.shoe));
			$('#total-shares-issued').html(get2DigitNumber(response.tbl_dict.total_shares_issued));
			$('#equity-gross-issue-calc').html('$&nbsp;' + get2DigitNumber(response.tbl_dict.gross_issue_price));
			$('#equity-net-issue-calc').html('$&nbsp;' + get2DigitNumber(response.tbl_dict.net_issue_price));
			$('#gross-proceeds').html(get2DigitNumber(response.tbl_dict.gross_proceeds));
			$('#net-proceeds').html(get2DigitNumber(response.tbl_dict.net_proceeds));
			
		});
	}

	const navTotalAssetAcquisition = (acqu_date, acqu_uses_choice, acqu_src_shares_fst, acqu_src_shares_sec, acqu_src_total, acqu_uses_acres, acqu_uses_ip30, acqu_uses_cost, acqu_uses_eur, acqu_uses_mboepd_total, acqu_uses_proved_mmboe_total, acqu_uses_f_d, acqu_uses_pud, acqu_uses_eur_mix, acqu_uses_mix, acqu_uses_proved_mix) => {
		sendRequest('navTotalAssetAcquisition/',
		{
			'acqu_date' :acqu_date,
			'acqu_uses_choice' : acqu_uses_choice,
			'acqu_src_shares_fst' : acqu_src_shares_fst,
			'acqu_src_shares_sec' : acqu_src_shares_sec,
			'acqu_src_total' : acqu_src_total,
			'acqu_uses_acres' : acqu_uses_acres,
			'acqu_uses_ip30' : acqu_uses_ip30,
			'acqu_uses_cost' : acqu_uses_cost,
			'acqu_uses_eur' : acqu_uses_eur,
			'acqu_uses_mboepd_total' : acqu_uses_mboepd_total,
			'acqu_uses_proved_mmboe_total' : acqu_uses_proved_mmboe_total,
			'acqu_uses_f_d' : acqu_uses_f_d,
			'acqu_uses_pud' : acqu_uses_pud,
			'acqu_uses_eur_mix' : acqu_uses_eur_mix,
			'acqu_uses_mix' : acqu_uses_mix,
			'acqu_uses_proved_mix' : acqu_uses_proved_mix,
		}, (response) => {
			$('#acquisition-source-shares-total').html('$&nbsp;' + get2DigitNumber(response.acqu_data.shares));
			$('#acquisition-source-cash').html('$&nbsp;' + get2DigitNumber(response.acqu_data.cash));
			$('#acquisition-uses-total').html('$&nbsp;' + get2DigitNumber(response.acqu_data.total));
			$('.acquisition-uses-mboepd').each(function(i, obj) {
				let data_id = parseInt($(this).attr('data-id'));
				let prod_mix = $(this)
				$.each(response.acqu_data.prod_mix, function(k, v) {
				    if (data_id == k) {
				    	prod_mix.html(get2DigitNumber(v));				    	
				    }
				});
			});
			$('.acquisition-uses-proved-mmboe').each(function(i, obj) {
				let data_id = parseInt($(this).attr('data-id'));
				let proved_mix = $(this)
				$.each(response.acqu_data.proved_mix, function(k, v) {
				    if (data_id == k) {
				    	proved_mix.html(get2DigitNumber(v));
				    }
				});
			});
			console.log(response.acqu_data.other_eur_mix)
			$('#acquisition-uses-eur-other').html(get2DigitNumber(response.acqu_data.other_eur_mix) + '&nbsp;%');
			$('#acquisition-uses-mix').html(get2DigitNumber(response.acqu_data.other_prod_mix) + '&nbsp;%');			
			$('#acquisition-uses-proved-mix').html(get2DigitNumber(response.acqu_data.other_proved_mix) + '&nbsp;%');
		});
	}

	// Asset Sale
	const navTotalAssetSale = (sale_date, sale_uses_choice,	sale_sources_total,	sale_src_acres, sale_src_ip30, sale_src_cost, sale_src_eur,	sale_src_mboepd_total, sale_src_proved_mmboe_total, sale_src_f_d, sale_src_pud,	sale_src_eur_mix, sale_src_mix,	sale_src_proved_mix) => {
		sendRequest('navTotalAssetSale/',
		{
			'sale_date' :sale_date,
			'sale_uses_choice' : sale_uses_choice,
			'sale_sources_total' : sale_sources_total,
			'sale_src_acres' : sale_src_acres,
			'sale_src_ip30' : sale_src_ip30,
			'sale_src_cost' : sale_src_cost,
			'sale_src_eur' : sale_src_eur,
			'sale_src_mboepd_total' : sale_src_mboepd_total,
			'sale_src_proved_mmboe_total' : sale_src_proved_mmboe_total,
			'sale_src_f_d' : sale_src_f_d,
			'sale_src_pud' : sale_src_pud,
			'sale_src_eur_mix' : sale_src_eur_mix,
			'sale_src_mix' : sale_src_mix,
			'sale_src_proved_mix' : sale_src_proved_mix,
		}, (response) => {

			$('#sale-sources-eur-other').html(get2DigitNumber(response.sale_data.other_eur_mix) + '&nbsp;%');
			$('#sale-sources-prod-mix-other').html(get2DigitNumber(response.sale_data.other_prod_mix) + '&nbsp;%');			
			$('#sale-sources-proved-mix').html(get2DigitNumber(response.sale_data.other_proved_mix) + '&nbsp;%');
			$('#sale-uses-cash-total').html('$&nbsp;' + get2DigitNumber(response.sale_data.total));
			$('#sale-uses-total').html('$&nbsp;' + get2DigitNumber(response.sale_data.total));
			$('.sale-sources-mboepd').each(function(i, obj) {
				let data_id = parseInt($(this).attr('data-id'));
				let prod_mix = $(this)
				$.each(response.sale_data.prod_mix, function(k, v) {
				    if (data_id == k) {
				    	prod_mix.html(get2DigitNumber(v));				    	
				    }
				});
			});
			$('.sale-sources-proved-mmboe').each(function(i, obj) {
				let data_id = parseInt($(this).attr('data-id'));
				let proved_mix = $(this)
				$.each(response.sale_data.proved_mix, function(k, v) {
				    if (data_id == k) {
				    	proved_mix.html(get2DigitNumber(v));
				    }
				});
			});
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
				total_duration = $("#total-duration").val(),
				total_year_define = $("#total-year-define").val(),
				total_boe_mcfe = $("#total-boe-mcfe").val();
				date = $('.value-summary-date').val()

			navTotalInitVariables(
				total_net_asset_value, 
				total_inflation, 
				total_rig, 
				total_duration, 
				total_year_define, 
				total_boe_mcfe,
				date
			)
				
		})

		.on('click', '#equity-offering-send-data', (event) => {
			let equity_choice = $('#equity-offering-choice').val(),
				equity_share_amount = $('#equity-share-amount').val(),
				equity_shoe = $('#equity-shoe').val(),
				equity_last_price = $('#equity-last-price').val(),
				equity_gross_issue = $('#equity-gross-issue').val(),
				equity_net_issue = $('#equity-net-issue').val(),
				date = $('.equity-offering-date').val();

			if (equity_choice == "" || equity_share_amount == "" || equity_shoe == "" || equity_gross_issue == "" || equity_net_issue == "" || equity_last_price == "") {
				alert("please fill in the all inputs.")
			}

			navTotalEquityOffering(equity_choice, equity_share_amount, equity_shoe, equity_last_price, equity_gross_issue, equity_net_issue, date)
		})

		.on('click', '#asset-acquisition-send-data', (event) => {
			let acqu_date = $('.asset-acquisition-date').val(),
				acqu_uses_choice = $('#acquisition-uses-choice').val(),
				acqu_src_shares_fst = $('#acquisition-source-shares-fst').val(),
				acqu_src_shares_sec = $('#acquisition-source-shares-sec').val(),
				acqu_src_total = $('#acquisition-source-total').val(),
				acqu_uses_acres = $('#acquisition-uses-acres').val(),
				acqu_uses_ip30 = $('#acquisition-uses-ip30').val(),
				acqu_uses_cost = $('#acquisition-uses-cost').val(),
				acqu_uses_eur = $('#acquisition-uses-eur').val(),
				acqu_uses_mboepd_total = $('#acquisition-uses-mboepd-total').val(),
				acqu_uses_proved_mmboe_total = $('#acquisition-uses-proved-mmboe-total').val(),
				acqu_uses_f_d = $('#acquisition-uses-f-d').val(),
				acqu_uses_pud = $('#acquisition-uses-pud').val(),
				
				acqu_uses_eur_mix = {};
				acqu_uses_mix = {};
				acqu_uses_proved_mix = {};
			console.log(acqu_uses_mboepd_total)
			$('.acquisition-uses-eur').each(function(i, obj) {
			    let tag_name = $(this).prop('tagName').toLowerCase();
			    let data_id = parseInt($(this).attr('data-id'));
			    if (tag_name != 'td') {
			    	acqu_uses_eur_mix[data_id] = $(this).val()
			    }			    
			});

			$('.acquisition-uses-mix').each(function(i, obj) {
			    let tag_name = $(this).prop('tagName').toLowerCase();
			    let data_id = parseInt($(this).attr('data-id'));
			    if (tag_name != 'td') {
			    	acqu_uses_mix[data_id] = $(this).val()
			    }			    
			});

			$('.acquisition-uses-proved-mix').each(function(i, obj) {
			    let tag_name = $(this).prop('tagName').toLowerCase();
			    let data_id = parseInt($(this).attr('data-id'));
			    if (tag_name != 'td') {
			    	acqu_uses_proved_mix[data_id] = $(this).val()
			    }			    
			});

			navTotalAssetAcquisition(
				acqu_date,
				acqu_uses_choice,
				acqu_src_shares_fst,
				acqu_src_shares_sec,
				acqu_src_total,
				acqu_uses_acres,
				acqu_uses_ip30,
				acqu_uses_cost,
				acqu_uses_eur,
				acqu_uses_mboepd_total,
				acqu_uses_proved_mmboe_total,
				acqu_uses_f_d,
				acqu_uses_pud,
				JSON.stringify(acqu_uses_eur_mix),
				JSON.stringify(acqu_uses_mix),
				JSON.stringify(acqu_uses_proved_mix),
			)		
		})

		// Asset Sale
		.on('click', '#asset-sale-send-data', (event) => {
			let sale_date = $('.asset-sale-date').val(),
				sale_uses_choice = $('#sale-uses-choice').val(),
				sale_sources_total = $('#sale-sources-total').val(),
				sale_src_acres = $('#sale-sources-acres').val(),
				sale_src_ip30 = $('#sale-sources-ip30').val(),
				sale_src_cost = $('#sale-sources-cost').val(),
				sale_src_eur = $('#sale-sources-eur').val(),
				sale_src_mboepd_total = $('#sale-sources-mboepd-total').val(),
				sale_src_proved_mmboe_total = $('#sale-sources-proved-mmboe-total').val(),
				sale_src_f_d = $('#sale-sources-f-d').val(),
				sale_src_pud = $('#sale-sources-pud').val(),
				
				sale_src_eur_mix = {};
				sale_src_mix = {};
				sale_src_proved_mix = {};

			$('.sale-sources-eur').each(function(i, obj) {
			    let tag_name = $(this).prop('tagName').toLowerCase();
			    let data_id = parseInt($(this).attr('data-id'));
			    if (tag_name != 'td') {
			    	sale_src_eur_mix[data_id] = $(this).val()
			    }			    
			});

			$('.sale-sources-mix').each(function(i, obj) {
			    let tag_name = $(this).prop('tagName').toLowerCase();
			    let data_id = parseInt($(this).attr('data-id'));
			    if (tag_name != 'td') {
			    	sale_src_mix[data_id] = $(this).val()
			    }			    
			});

			$('.sale-sources-proved-mix').each(function(i, obj) {
			    let tag_name = $(this).prop('tagName').toLowerCase();
			    let data_id = parseInt($(this).attr('data-id'));
			    if (tag_name != 'td') {
			    	sale_src_proved_mix[data_id] = $(this).val()
			    }			    
			});

			navTotalAssetSale(
				sale_date,
				sale_uses_choice,
				sale_sources_total,
				sale_src_acres,
				sale_src_ip30,
				sale_src_cost,
				sale_src_eur,
				sale_src_mboepd_total,
				sale_src_proved_mmboe_total,
				sale_src_f_d,
				sale_src_pud,
				JSON.stringify(sale_src_eur_mix),
				JSON.stringify(sale_src_mix),
				JSON.stringify(sale_src_proved_mix),
			)		
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