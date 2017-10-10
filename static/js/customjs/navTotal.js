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
			$('#total-ngl-percent').html(get2DigitNumber(response.init_data.wti) + '&nbsp;%')
			$('#total-r').html(get2DigitNumber(response.init_data.r))
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
			$('#shares_out').html(response.shares_out);
			window.footerData = response.proved_reserves
			window.provedReserve.rows().remove().draw();
			window.provedReserve.row.add(response.proved_reserves).draw();
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
			
			$('#acquisition-uses-eur-other').html(get2DigitNumber(response.acqu_data.other_eur_mix) + '&nbsp;%');
			$('#acquisition-uses-mix').html(get2DigitNumber(response.acqu_data.other_prod_mix) + '&nbsp;%');			
			$('#acquisition-uses-proved-mix').html(get2DigitNumber(response.acqu_data.other_proved_mix) + '&nbsp;%');
			$('#shares_out').html(response.shares_out)
			window.footerData = response.proved_reserves
			window.provedReserve.rows().remove().draw();
			window.provedReserve.row.add(response.proved_reserves).draw();
		});
	}

	// ================================= Asset Sale ===================================================
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

	// ================================= NavTotal NET Lading --===========================================
	const navTotalNetLanding = (sale_proceeds_s, sale_carries_s, equity_s, monies_s, carries_s) => {
		sendRequest('navTotalNetLanding/', {
			'sale_proceeds_s' : sale_proceeds_s,
			'sale_carries_s' : sale_carries_s,
			'equity_s' : equity_s,
			'monies_s' : monies_s,
			'carries_s' : carries_s,
		}, (response) => {
			console.log(response.net_landing)
			$('#sale-proceeds-mm').html('$&nbsp;' + get2DigitNumber(response.net_landing.sale_proceeds_p))
			$('#sale-proceeds-xp').html('$&nbsp;' + get2DigitNumber(response.net_landing.sale_proceeds_xp))
			$('#sale-carries-xp').html('$&nbsp;' + get2DigitNumber(response.net_landing.sale_carries_xp))
			$('#equity-mm').html('$&nbsp;' + get2DigitNumber(response.net_landing.equity_p))
			$('#equity-xp').html('$&nbsp;' + get2DigitNumber(response.net_landing.equity_xp))
			$('#carries-xp').html('$&nbsp;' + get2DigitNumber(response.net_landing.carries_xp))
			$('#monies-mm').html('$&nbsp;' + get2DigitNumber(response.net_landing.monies_p))
			$('#monies-xp').html('$&nbsp;' + get2DigitNumber(response.net_landing.monies_xp))
			$('#sale-net').html('$&nbsp;' + get2DigitNumber(response.net_landing.sale_net))
			$('#purchase-net').html('$&nbsp;' + get2DigitNumber(response.net_landing.purchase_net))
			window.otherAssetFooterData = response.other_asset
			window.totalProved.rows().remove().draw();
			window.totalProved.row.add(response.other_asset).draw();
		})
	}
	
	// ================================= NavTotal Lading Results ===========================================
	const navTotalLandingResult = (landing_debt, landing_equivalents, landing_deficit, landing_hedge) => {
		sendRequest('navTotalLandingResults/', {
			'debt' : landing_debt,
			'equivalents' : landing_equivalents,
			'deficit' : landing_deficit,
			'hedge' : landing_hedge,
		}, (response) => {
			$('#share-debt').html('$&nbsp;' + get2DigitNumber(response.calc_results.debt))
			$('#share-equivalents').html('$&nbsp;' + get2DigitNumber(response.calc_results.equivalents))
			$('#share-deficit').html('$&nbsp;' + get2DigitNumber(response.calc_results.deficit))
			$('#share-hedge').html('$&nbsp;' + get2DigitNumber(response.calc_results.hedge))
			$('#total-mm-liabilities').html('$&nbsp;' + get2DigitNumber(response.calc_results.total_mm_liabilities))
			$('#total-share-liabilities').html('$&nbsp;' + get2DigitNumber(response.calc_results.total_share_liabilities))
			$('#proven-net-mm').html('$&nbsp;' + get2DigitNumber(response.calc_results.proven_net_mm))
			$('#proven-net-share').html('$&nbsp;' + get2DigitNumber(response.calc_results.proven_net_share))
		})
	}

	// ================================= NavTotal Unconventional ===========================================
	const navTotalUnconventional = (acre_unconv, risk_unconv, spacing, zone, zone_pros, rigs, days_to, drilled) => {
		sendRequest('navTotalUnconventional/', {
			'acre_unconv' : acre_unconv,
			'risk_unconv' : risk_unconv,
			'spacing' : spacing,
			'zone' : zone,
			'zone_pros' : zone_pros,
			'rigs' : rigs,
			'days_to' : days_to,
			'drilled' : drilled
		}, (response) => {
			row = []
			window.unconventionalFooterData = response.calc_result['array']
			window.addPlayUnconventional.rows().remove().draw();
			for (let i = 0; i < response.calc_result['array'].length; i ++) {
				row.push(get2DigitNumber(response.calc_result['array'][i]))
			}
			window.addPlayUnconventional.row.add(row).draw();
			$('.net_resource').each(function (i, obj) {
				let data_id = parseInt($(this).attr('data-id'));
				$(this).html(get2DigitNumber(response.calc_result['dict'][data_id]))
			});
			console.log(response.calc_result['dict'])
			$('#unconventional-acre').html('$&nbsp;' + get2DigitNumber(response.calc_result['dict']['acre']) + '/acre');
			$('#unconventional-acreage').html(get2DigitNumber(response.calc_result['dict']['acerage']));
			$('#unconventional-wells').html(get2DigitNumber(response.calc_result['dict']['wells']));
			$('#unconventional-well-cost').html('$&nbsp;' + get2DigitNumber(response.calc_result['dict']['well_cost']));
			$('#unconventional-pv10').html('$&nbsp;' + get2DigitNumber(response.calc_result['dict']['well_pv_ten']));
			$('#unconventional-pv-boe').html('$&nbsp;' + get2DigitNumber(response.calc_result['dict']['well_pv_eur']));
			$('#unconventional-irr').html(get2DigitNumber(response.calc_result['dict']['irr']) + '&nbsp;%');
			$('#unconventional-wells-yr').html(get2DigitNumber(response.calc_result['dict']['wells_yr']));
			$('#unconventional-years').html(get2DigitNumber(response.calc_result['dict']['years_unconv']));
			$('#unconventional-m-a').html(get2DigitNumber(response.calc_result['dict']['m_a']));
		})
	}

	// ================================ NAV Total Conventional ===========================================
	const navTotalConventional = (lst_hc, flat, lst_prod, dev_cost, wl, operator, royalty, trap, reservoir, seal, timing, commercial, closure, drainage, mean, boe_feet, oil_conv, gas_conv, risk_conv, proved_book) => {
		sendRequest('navTotalConventional/', {
			'lst_hc' : lst_hc,
			'flat' : flat,
			'lst_prod' : lst_prod,
			'dev_cost' : dev_cost,
			'wl' : wl,
			'operator' : operator,
			'royalty' : royalty,
			'trap' : trap,
			'reservoir' : reservoir,
			'seal' : seal,
			'timing' : timing,
			'commercial' : commercial,
			'closure' : closure,
			'drainage' : drainage,
			'mean' : mean,
			'boe_feet' : boe_feet,
			'oil_conv' : oil_conv,
			'gas_conv' : gas_conv,
			'risk_conv' : risk_conv,
			'proved_book' : proved_book,
		}, (response) => {
			row = []
			window.conventionalFooterData = response.calc_result['array']
			window.addPlayConventional.rows().remove().draw();
			for (let i = 0; i < response.calc_result['array'].length; i ++) {
				row.push(get2DigitNumber(response.calc_result['array'][i]))
			}
			window.addPlayConventional.row.add(row).draw();
		})
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

		// ================================ Asset Sale ===================================================
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

		// ======================================== Change P(s) ============================================
		.on("click", "#landing-net-change-btn", (event) => {
			let sale_proceeds_s = $('#sale-proceeds-s').val(),
				sale_carries_s = $('#sale-carries-s').val(),
				equity_s = $('#equity-s').val(),
				monies_s = $('#monies-s').val(),
				carries_s = $('#carries-s').val();

			if (sale_proceeds_s == "" || sale_carries_s == "" || equity_s == "" || monies_s == "" || carries_s == "") {
				alert("please fill in the all inputs.")
			}

			navTotalNetLanding(
					sale_proceeds_s,
					sale_carries_s,
					equity_s,
					monies_s,
					carries_s
				)
		})

		// ==================================== Landing Results =========================================
		.on("click", "#landing-results-btn", (event) => {
			let landing_debt = $('#landing-debt').val(),
				landing_equivalents = $('#landing-equivalents').val(),
				landing_deficit = $('#landing-deficit').val(),
				landing_hedge = $('#landing-hedge').val();

			if (landing_debt == "" || landing_equivalents == "" || landing_deficit == "") {
				alert("please fill in the all inputs.")
			}

			navTotalLandingResult(
					landing_debt,
					landing_equivalents,
					landing_deficit,
					landing_hedge
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

		// ==================================== Unconventional =========================================
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
			navTotalUnconventional(
					acre_unconv, 
					risk_unconv, 
					spacing,
					zone, 
					zone_pros, 
					rigs, 
					days_to, 
					drilled
				);
		})

		// ==================================== Conventional =========================================
		.on('click', '#conventional-view', (event) => {
			let lst_hc = $('#lst-hc').val(),
				flat = $('#flat').val(),
				lst_prod = $('#lst-prod').val(),
				dev_cost = $('#dev-cost').val(),
				wl = $('#wl').val(),
				operator = $('#operator').val(),
				royalty = $('#royalty').val(),
				trap = $('#trap').val(),
				reservoir = $('#reservoir').val(),
				seal = $('#seal').val(),
				timing = $('#timing').val(),
				commercial = $('#commercial').val(),
				closure = $('#closure').val(),
				drainage = $('#drainage').val(),
				mean = $('#mean').val(),
				boe_feet = $('#boe-feet').val(),
				oil_conv = $('#oil-conv').val(),
				gas_conv = $('#gas-conv').val(),
				risk_conv = $('#risk-conv').val(),
				proved_book = $('#proved-book').val();

			if (lst_hc == "" || flat == "" || lst_prod == "" || dev_cost == "" || wl == "" || operator == "" || royalty == "" || trap == "" || reservoir == "" || seal == "" || timing == "" || commercial == "" || closure == "" || drainage == "" || mean == "" || boe_feet == "" ||  oil_conv == "" || gas_conv == "" || risk_conv == "" || proved_book == "") {
				alert("please fill in the all inputs.")
			}
			navTotalConventional(
					lst_hc,
					flat,
					lst_prod,
					dev_cost,
					wl,
					operator,
					royalty,
					trap,
					reservoir,
					seal,
					timing,
					commercial,
					closure,
					drainage,
					mean,
					boe_feet,
					oil_conv,
					gas_conv,
					risk_conv,
					proved_book
				);
		})

		window.provedReserve = $('#proved-reserves').DataTable({
			"scrollX": true,
			"paging": false,
			"searching": false,
			"fnFooterCallback": function( nFoot, aData, iStart, iEnd, aiDisplay ) {
				let api = this.api()
				for (let i = 0; window.footerData && i < window.footerData.length; i ++){
					api.column(i).footer().innerHTML = (window.footerData) ? window.footerData[i] : 0
				}
			}
		});

		window.totalProved = $("#total-proved").DataTable({
			"scrollX": true,
			"paging" : false,
			"searching" : false,
			"fnFooterCallback": function( nFoot, aData, iStart, iEnd, aiDisplay ) {
				let api = this.api()
				for (let i = 0; window.otherAssetFooterData && i < window.otherAssetFooterData.length; i ++){
					api.column(i).footer().innerHTML = (window.otherAssetFooterData) ? window.otherAssetFooterData[i] : 0
				}
			}
		})

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