BOL.sentences = function (text_no) {
    var s = {
        'de': ["Anzahl gefundene Individuen: ", "Fundorte des Taxons auf der Karte zeigen",
            "Auf Datenpunkt klicken, um die Arten anzuzeigen"],
        'en': ["Number of specimens found: ", "Display locations of the taxon in the map",
            "Click on datapoint to display the species names"]

    };
    return s[this.lang][text_no];
};

(function ($) {
    var map;
    startSearch = function () {
        var _id = document.getElementById('searchCaption').value,
            _category = document.getElementById('searchCategory').value, page;
        showLoadingAnimation(page = "MAP");
        $.ajax({
            url: "/static/getSpecimenGeoInfo",
            type: 'POST',
            dataType: 'json',
            data: {
                id: _id, category: _category, user_id: document.getElementById('option-user').value,
                lan: BOL.get_lang()
            },
            success: function (data) {
                if (!data.success) {
                    alert(data.text);
                }
                createFundstellenLayers(data);
                hideLoadingAnimation(page = "MAP");
                createAnzeige(data);
            },
            error: function (xhr, textStatus, errorThrown) {
                hideLoadingAnimation(page = "MAP");
            }
        });
    };

    function fillOptions() {
        $.ajax({
            url: "/static/fillOptions",
            type: 'POST',
            dataType: 'html',
            data: {user_id: document.getElementById('option-user').value, lan: BOL.get_lang()},
            error: function (xhr, status, error) {
                //alert(status);
                alert(xhr.responseText);
            },
            success: function (html) {
                var dropDown = $('#searchCategory').append(html);
            }
        });
    }

    submitTextBox = function (key) {
        if (key.which == 13) {
            startSearch();
        }
    };

    after_load = function () {
        BOL.set_lang($(document.body).attr('data-lang'));
        jQuery.ajax({
            url: "/static/loadTreeView",
            type: 'POST',
            dataType: 'json',
            data: {nodeid: 1, user_id: document.getElementById('option-user').value, lan: BOL.get_lang()},
            success: function (data) {
                if (!data.success) {
                    alert(data.text);
                } else {
                    createTreeView(data.entries);
                }
            },
            error: function (xhr, textStatus, errorThrown) {
                alert(textStatus);
            }
        });
        map_init();
        fillOptions();
    };

    function createTreeView(rows) {
        for (var i = 0; i < rows.length; i++) {
            addNode(rows[i]);
        }
    }

    loadTreeview = function (element) {
        var childid = ".ParentNode_" + $(element).attr('node');
        if ($(childid).css("display") == "none") {
            $(childid).css("display", "block");
        } else {
            $(childid).css("display", "none");
        }

        var prefix = document.getElementById("prefix_" + $(element).attr('node'));
        if ($(prefix).hasClass("closed")) {
            prefix.innerHTML = " - ";
            prefix.className = "expanded";
        } else if ($(prefix).hasClass("expanded")) {
            prefix.innerHTML = " + ";
            prefix.className = "closed";
        }

        if (!$(element).hasClass("clicked")) {
            $.ajax({
                url: "/static/loadTreeView",
                type: 'POST',
                dataType: 'json',
                data: {
                    nodeid: $(element).attr('taxa'),
                    user_id: document.getElementById('option-user').value,
                    lan: BOL.get_lang()
                },
                success: function (data) {
                    if (!data.success) {
                        alert(data.text);
                    } else {
                        createTreeView(data.entries);
                    }
                },
                error: function (xhr, textStatus, errorThrown) {
                    //
                    alert(textStatus);
                }
            });
            $(element).addClass("clicked");
        }
    }

    searchTaxa = function (element) {
        var _taxa = $(element).attr('taxa');
        document.getElementById("anzeige-content").innerHTML = "";
        showLoadingAnimation(page = "MAP");
        $.ajax({
            url: "/static/getSpecimenGeoInfo",
            type: 'POST',
            dataType: 'json',
            data: {
                id: _taxa,
                category: "treeview",
                user_id: document.getElementById('option-user').value,
                lan: BOL.get_lang()
            },
            success: function (data) {
                if (!data.success) {
                    alert(data.text);
                    createFundstellenLayers(data);
                }
                hideLoadingAnimation(page = "MAP");
                createFundstellenLayers(data);
                createAnzeige(data);
            },
            error: function (xhr, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
        var suchBegriff = document.getElementById('searchCaption');
        var suchKategorie = document.getElementById('searchCategory');
        suchBegriff.value = $(element).attr('caption');
        suchKategorie.value = "Taxon Name";
    }

    function addNode(row) {
        // ["Animalia",  1,         2,     3,         4,      5,                      6,                   7,    8, 9]
        // taxon      , id, parent_id, known, collected, barcode, collected_individuals, barcode_individuals, rank, vernacular
        var rootNodeId, newNode = new Array(), newNodeId, newNodeValue, nodePrefix, arrNode = '',
            collInd = '', barInd = '',
            taxon_id, vernacular;
        if (row[2] == 1) {
            rootNodeId = "Node_Root";
        } else {
            rootNodeId = "Node_" + row[2];
        }
        newNodeId = "Node_" + row[1];
        if (row[4] > 0) {
            collInd = '('.concat(String(row[6]), ') ');
        }
        if (row[7] > 0) {
            barInd = '('.concat(String(row[7]), ') ');
        }
        taxon_id = row[1];
        if (row[9]) {
            vernacular = '('.concat(String(row[9]), ') ');
        } else {
            vernacular = '';
        }
        var newNodeValueClass = ''
        if (row[8] != 1) {
            newNodeValueClass = "clr_red";
        }
        newNodeValue = '<span'.concat(' class="', newNodeValueClass, '">', row[0], '</span> ', vernacular, ' <span class="treeview-red">', String(row[3]), '</span>/<span class="treeview-orange">', String(row[4]), collInd, '</span>/<span class="treeview-green">', String(row[5]), barInd, '</span>');
        newNode = ['<ul id="' + newNodeId + '"'];
        if (row[2] > 1) {
            newNode.push('class="ParentNode_'.concat(rootNodeId, ' childNode"'));
        }
        newNode.push('>');
        newNode.push('<li>');

        nodePrefix = " ", nodeClass = "no_child";
        if (row[8] != 1) {  // rank: 1=leaf node
            nodePrefix = " +  ";
            nodeClass = "closed clr_red";
        }
        newNode.push('<a node="'.concat(newNodeId, '" taxa="', taxon_id, '" onclick="loadTreeview(this)"'));

        if (row[4]) {
            newNode.push(' class="taxa_known"');
            if (row[4] < 1000) {
                arrNode = '<a taxa="'.concat(taxon_id, '" onclick="searchTaxa(this)" caption="', row[0], '" class="taxon_arrow taxa_known" title="Display locations of the taxon in the map"> &#8594</a>');
            }
        }
        newNode.push('>');
        newNode.push('<span id="prefix_'.concat(newNodeId, '" class="', nodeClass, '">', nodePrefix, "</span>", newNodeValue));
        newNode.push('</a>'.concat(arrNode, '</li>'));
        newNode.push('</ul>');
        $rootNode = $('#' + rootNodeId).append(newNode.join(""));
    }

    function showLoadingAnimation(page) {
        $("#loadingSearch" + page).removeClass('hidden');
    }

    function hideLoadingAnimation(page) {
        $("#loadingSearch" + page).addClass('hidden');
    }

    /* ============ MAP ============== */
    var source, clusterSource, vectorLayer;

    function createFundstellenLayers(data) {
        if (vectorLayer) {
            map.removeLayer(vectorLayer);
        }
        if (data.entries.length > 0) {
            polygonLayer(data.entries, data.bounds);
        }
    }

    function transform(lat, lon) {
        //return [lat, lon]
        return ol.proj.transform([lat, lon], 'EPSG:4326', 'EPSG:3857');
    }

    function calc_extend(bounds) {
        var bottomLeft = transform(bounds[1], bounds[0]),
            topRight = transform(bounds[3], bounds[2]);
        return new ol.extent.boundingExtent([bottomLeft, topRight]);
    }

    var raster = new ol.layer.Tile({
        source: new ol.source.OSM()
    });

    var stateLayer = new ol.layer.Vector({
        source: new ol.source.GeoJSON({
            projection: 'EPSG:3857',
            url: '/static/layers/states.geojson	'
        }),
        style: new ol.style.Style({
            stroke: new ol.style.Stroke({color: 'rgba(255,255,255,0.63)', width: 1})
        })
    });

    function map_init() {
        var boundsWelt = [-180, -90, 180, 90],
            boundsD = [5.5, 47.0, 15.0, 55.5],
            boundsE = [-10.19, 27.59, 62.93, 74.69];

        map = new ol.Map({
            target: 'map',
            renderer: 'canvas',
            layers: [raster, stateLayer],
            view: new ol.View({
                //projection: 'EPSG:4326',
                center: transform(10.2, 49.6),
                zoom: 4
            }),
            controls: ol.control.defaults({
                attributionOptions: ({
                    collapsible: false
                })
            })
        });
        //map.addControl(new ol.control.MousePosition());
        document.getElementById('map_info').innerHTML = BOL.sentences(2);
    }

    function changeMapSize() {
        map.updateSize();
    }

    function polygonLayer(entries, bounds) {
        var user_id = document.getElementById('option-user').value;
        String.prototype.trim = function () {
            return this.replace(/^\s+|\s+$/g, "")
        };

        if (entries.length == 0) {
            return;
        }

        var styleCache = {},
            e, i,
            lon, lat,
            count = entries.length,
            features = new Array();

        for (i = 0; i < count; i++) {
            e = entries[i];
            lat = parseFloat(e.coord[1]);
            lon = parseFloat(e.coord[0]);
            if (isNaN(lon) || isNaN(lat)) continue;

            features.push(new ol.Feature({
                geometry: new ol.geom.Point(transform(lat, lon)),
                name: e.species,
                id: e.id
            }));
        }

        if (features.length == 0) {
            return;
        }

        source = new ol.source.Vector({
            features: features
        });

        clusterSource = new ol.source.Cluster({
            distance: 40,
            source: source
            //projection: ....
            //extend: ...
        });

        vectorLayer = new ol.layer.Vector({
            title: "Sampling",
            source: clusterSource,
            style: function (feature, resolution) {
                var size = feature.get('features').length;
                var style = styleCache[size];
                if (!style) {
                    style = [new ol.style.Style({
                        image: new ol.style.Circle({
                            radius: 10,
                            stroke: new ol.style.Stroke({
                                color: '#222',
                                width: 1
                            }),
                            fill: new ol.style.Fill({
                                color: 'rgba(255, 143, 53, 0.68)'
                            })
                        }),
                        text: new ol.style.Text({
                            text: size.toString(),
                            fill: new ol.style.Fill({
                                color: '#fff'
                            })
                        })
                    })];
                    styleCache[size] = style;
                }
                return style;
            }
        });

        map.addLayer(vectorLayer);

        //vectorLayer.getSource().getExtent();
        var extent = calc_extend(bounds);
        map.getView().fitExtent(extent, map.getSize());

        $(map.getViewport()).on('click', function (evt) {
            var pixel = map.getEventPixel(evt.originalEvent);
            displayFeatureInfo(pixel);
        });
    }

    var highlightStyleCache = {};
    var featureOverlay = new ol.FeatureOverlay({
        map: map,
        style: function (feature, resolution) {
            var size = feature.get('features').length;
            if (!highlightStyleCache[text]) {
                highlightStyleCache[text] = [new ol.style.Style({
                    image: new ol.style.Circle({
                        radius: 10,
                        stroke: new ol.style.Stroke({
                            color: '#f00',
                            width: 1
                        }),
                        fill: new ol.style.Fill({
                            color: 'rgba(255,0,0,0.1)'
                        })
                    }),
                    text: new ol.style.Text({
                        text: size.toString(),
                        fill: new ol.style.Fill({
                            color: '#000'
                        }),
                        stroke: new ol.style.Stroke({
                            color: '#f00',
                            width: 3
                        })
                    })
                })];
            }
            return highlightStyleCache[text];
        }
    });

    var highlight;
    var displayFeatureInfo = function (pixel) {
        var features = [],
            info = {}, f, i, j, n, t = [];
        map.forEachFeatureAtPixel(pixel, function (feature, layer) {
            features.push(feature);
        });
        if (features.length > 0) {
            f = features[0].get('features');  // first layer = datapoints
            for (j = 0; j < f.length; j++) {
                n = f[j].get('name');
                if (!info[n]) {
                    info[n] = 0;
                }
                info[n] = info[n] + 1;
            }
            $.each(info, function (key, value) {
                t.push(key + ': ' + value);
            });
        }
        if (t.length > 0) {
            document.getElementById('map_info').innerHTML = t.join(', ') || '(unknown)';
            if (features[0] !== highlight) {
                if (highlight) {
                    featureOverlay.removeFeature(highlight);
                }
                if (features[0]) {
                    featureOverlay.addFeature(features[0]);
                }
                highlight = features[0];
            }
        } else {
            document.getElementById('map_info').innerHTML = BOL.sentences(2);
        }
        features = [], info = {}
    };

    expandMap = function (expand) {
        var $treeview = $('#mittlerer_Teil_links'),
            $divmap = $('#mittlerer_Teil_rechts'),
            $plusButton = $('#mapPlus'),
            $minusButton = $('#mapMinus');
        if (expand) {
            $treeview.addClass("hidden");
            $divmap.addClass("enlargeMap");
            $plusButton.addClass("hidden");
            $minusButton.removeClass("hidden");
        } else {
            $treeview.removeClass("hidden");
            $divmap.removeClass("enlargeMap");
            $plusButton.removeClass("hidden");
            $minusButton.addClass("hidden");
        }
        changeMapSize();
    };

    /* ============ Search results ============== */
    function createAnzeige(data) {
        var e, i = 0, j, l = data.entries.length,
            lang = data.lang, id,
            barcode_present = ['&#10007;', '&#8730;'];
        createTableHeader(data.fields);



	var tabledata = [];
        for ( var i=0 ; i<l; i++ ) {
	    e = data.entries[i];
	    tablerow = {};

	    if (e.barcode != '0') {
                tablerow['DT_RowClass'] = 'has_barcode';
            }

	    for (var j=0; j < data.fields.length; j++) {
		id = data.fields[j][0];

                if (id == 93) {
                    tablerow[j] = barcode_present[e.barcode];
                } else if (id == 27) {
                    tablerow[j] = e.species;
                } else if (id == 28) {
                    tablerow[j] = e.vernacular;
                } else if (id == 19) {
                    tablerow[j] = e.taxon;
                } else if (id == 22) {
                    tablerow[j] = e.institute;
                } else {
                    if (e.data[id]) {
                        tablerow[j] = e.data[id];
                    } else {
                        tablerow[j] = '';
                    }
                }
	    }
	    tabledata.push(tablerow);
	}


	var tablecolumns = [];

	for (var j=0; j < data.fields.length; j++) {
	    // generate array of {tabledata: 'index'} objects  
	    tablecolumns.push({'data': j})
	}


        if (i > 0) {

	    // set table generation parameters depending on row number
	    var paging = false;
	    var defrender = false;
	    var scroller = false;
	    if (i > 10000) {
		paging = true;
		defrender = true;
		//scroller = {
		//    loadingIndicator: true 
		//}
		// switch line break off in cells to enable scrollers.js deferred loading capabilities
		//$('.dataTable').css('white-space', 'nowrap');
	    }


            var resulttable = $('#viewTable').DataTable({
		'data': tabledata,
		'columns': tablecolumns,
		// try scroller
		"scroller": scroller,
		"deferRender": defrender,
                "pagingType": "full_numbers",
                "scrollX": true,
                "scrollY": 200,
                "scrollCollapse": false,
                "paging": paging,
		"lengthMenu": [ 10, 50, 100, 500, 1000 ],
		//wait 400ms between each keypress adding a letter in search field 
		"searchDelay": 400,
		// pageLength is set below because of performance problems when set here
		//"pageLength": "100",
                "language": {
                    "url": "/static/js/DataTables/" + BOL.get_lang() + ".txt"
                }
                //"order": [[1, "asc"]]
            });

	    // setting pageLength in parameters kills performance when loading new pages
	    resulttable.page.len(1000).draw;

           $("#viewTable").removeClass('hidden');
            $("#viewCounter").html(BOL.sentences(0) + i);
        }
    }



/* this was: loading html first and than style tha table with DataTables
        for (i; i < l; i++) {
            e = data.entries[i]
            if (e.barcode != '0') {
                dataRow += '<tr class="has_barcode">';
            } else {
                dataRow += '<tr>';
            }
            for (j = 0; j < data.fields.length; j++) {
                id = data.fields[j][0];  // field[id, name]
                if (id == 93) {
                    dataRow += '<td class="tableRow1">' + barcode_present[e.barcode] + '</td>'
                } else if (id == 27) {
                    dataRow += '<td class="tableRow1">' + e.species + '</td>'
                } else if (id == 28) {
                    dataRow += '<td class="tableRow2">' + e.vernacular + '</td>'
                } else if (id == 19) {
                    dataRow += '<td class="tableRow2">' + e.taxon + '</td>'
                } else if (id == 22) {
                    dataRow += '<td class="tableRow2">' + e.institute + '</td>'
                } else {
                    if (e.data[id]) {
                        dataRow += '<td class="tableRow2">' + e.data[id] + '</td>';
                    } else {
                        dataRow += '<td class="tableRow2"></td>';
                    }
                }
            }
            dataRow += '</tr>';
        }
        if (i > 0) {
            document.getElementById("viewTableData").innerHTML = dataRow;
            $('#viewTable').DataTable({
                "pagingType": "full_numbers",
                "scrollX": true,
                "scrollY": "200px",
                "scrollCollapse": true,
                "paging": false,
                "language": {
                    "url": "/static/js/DataTables/" + BOL.get_lang() + ".txt"
                },
                "order": [[1, "asc"]]
            });
            $("#viewTable").removeClass('hidden');
            $("#viewCounter").html(BOL.sentences(0) + i);
        }
    }
*/

    function createTableHeader(fields) {
        var id, name,
            t = '<a id="viewCounter">' + BOL.sentences(0) + '0 <br> </a><div id="resultArea"><table id="viewTable" class="display"><thead><tr>';
        for (j = 0; j < fields.length; j++) {
            id = fields[j][0];
            name = fields[j][1];
            if (id == 27) {
                t += '<th class="tableRow1">' + name + '</th>'
            } else {
                t += '<th class="tableRow2">' + name + '</th>'
            }
        }
        t += '</tr></thead><tbody id="viewTableData"></tbody></table></div>'
        document.getElementById("anzeige-content").innerHTML = t
    }

    function selectMapLayer(layerId) {
        var style = new OpenLayers.Style({
                    strokeColor: "white",
                    strokeWidth: 1,
                    fillColor: "blue",
                    fillOpacity: 0.4,
                    fontColor: "white",
                    fontSize: 9
                }
            ),
            styleMap = new OpenLayers.StyleMap({"default": style});
        if (map.layers[layerId]) {
            map.layers[layerId].styleMap = styleMap;
            map.layers[layerId].redraw();
        }
    }

    function deselectMapLayer(layerId) {
        var style = new OpenLayers.Style({
                    strokeColor: "white",
                    strokeWidth: 1,
                    fillColor: "#FF8F35",
                    fillOpacity: 0.4,
                    fontColor: "white",
                    fontSize: 9
                }
            ),
            styleMap = new OpenLayers.StyleMap({"default": style});
        if (map.layers[layerId]) {
            map.layers[layerId].styleMap = styleMap;
            map.layers[layerId].redraw();
        }
    }

    csvExport = function () {
        var _caption = document.getElementById('searchCaption').value,
            _category = document.getElementById('searchCategory').value;
        $.ajax({
            url: "/static/csvExport",
            type: 'POST',
            data: {
                caption: _caption,
                category: _category,
                user_id: document.getElementById('option-user').value,
                lan: BOL.get_lang()
            },
            dataType: 'json',
            success: function (data) {
                if (!data.success) {
                    alert(data.text);
                } else {
                    populateIframe("frame1", data.filename)
                }
            },
            error: function (xhr, textStatus, errorThrown) {
                alert("Fehler beim Erstellen der Datei")
            }
        });
    };

    function populateIframe(id, path) {
        var ifrm = document.getElementById(id);
        ifrm.src = "/download?fileName=" + path;
    }

    hideButton = function (page) {
        $("#op" + page).prop("disabled", true);
        $('select').change(
            function () {
                if (page == "DE") {
                    if ($("div.choiceTaxaDE_value").text() == "not_chosen_ta") {
                        $("#opDE").prop("disabled", true);
                    }
                    else {
                        $("#opDE").prop("disabled", false);
                    }
                } else if (page == "BL") {
                    if ($("div.choiceTaxaBL_value").text() == "not_chosen_ta" || $("#choiceStateBL").val() == "None") {
                        $("#opBL").prop("disabled", true);
                    }
                    else {
                        $("#opBL").prop("disabled", false);
                    }
                } else if (page == "MI") {
                    if ($("div.choiceTaxaMI_value").text() == "not_chosen_ta") {
                        $("#opMI").prop("disabled", true);
                    }
                    else {
                        $("#opMI").prop("disabled", false);
                    }
                }
            }
        );
    }

    /* ============ Statistics Germany ============== */

    autocomplete = function (page) {
        $.ajax({
            url: "/static/autocomplete_statistics",
            dataType: "json",
            success: function (response) {
                var data = $(response).map(function () {
                    return {value: this.taxon, id: this.id + ";" + this.lft + ";" + this.rgt};
                }).get();

                if (page=='DE') {
                    $("#StatisticsDE #choiceTaxaDE").autocomplete({
                        source: data,
                        minLength: 0,
                        select: function (event, ui) {
                            $('#choiceTaxaDE_value').text(ui.item.id);
                            $('#opDE').prop("disabled", false)
                        }
                    });
                } else if (page=='MI') {
                    $("#Missing #choiceTaxaMI").autocomplete({
                        source: data,
                        minLength: 0,
                        select: function (event, ui) {
                            $('#choiceTaxaMI_value').text(ui.item.id);
                            $('#opMI').prop("disabled", false)
                        }
                    });
                } else if (page=='BL') {
                    $("#StatisticsBL #choiceTaxaBL").autocomplete({
                        source: data,
                        minLength: 0,
                        select: function (event, ui) {
                            $('#choiceTaxaBL_value').text(ui.item.id);
                            $('#opBL').prop("disabled", false)
                        }
                    });
                }
            }
        });
    };

    ajaxDataRendererDE = function (lang, taxon) {
        var choiceTaxaDE = $('#choiceTaxaDE_value').text(),
            table_data,
            table_data_all_pivot,
            language;
        if (lang == 'de') {
            table_data_all_pivot = [['<div><h2>&Uuml;bersicht der gesammelten '] + taxon +
            [' in den Bundesl&auml;ndern</h2></div>' +
            '<table id="datatableDE" class="display compact" cellspacing="0" width="100%">' +
            '<thead><tr><th>Art</th><th>EU</th><th>BW</th><th>BY</th><th>BE</th><th>BB</th><th>HB</th><th>HH</th>' +
            '<th>HE</th><th>MV</th><th>NI</th><th>NW</th><th>RP</th><th>SL</th><th>SN</th><th>ST</th>' +
            '<th>SH</th><th>TH</th></tr></thead><tfoot><tr><th>Art</th><th>EU</th><th>BW</th><th>BY</th>' +
            '<th>BE</th><th>BB</th><th>HB</th><th>HH</th><th>HE</th><th>MV</th><th>NI</th><th>NW</th><th>RP</th>' +
            '<th>SL</th><th>SN</th><th>ST</th><th>SH</th><th>TH</th></tr></tfoot><tbody>']];
        } else {
            table_data_all_pivot = [['<div><h2>List of collected '] + taxon +
            [' in the federal states of Germany</h2></div>' +
            '<table id="datatableDE" class="display compact" cellspacing="0" width="100%">' +
            '<thead><tr><th>Species</th><th>EU</th><th>BW</th><th>BY</th><th>BE</th><th>BB</th><th>HB</th><th>HH</th>' +
            '<th>HE</th><th>MV</th><th>NI</th><th>NW</th><th>RP</th><th>SL</th><th>SN</th><th>ST</th><th>SH</th>' +
            '<th>TH</th></tr></thead><tfoot><tr><th>Species</th><th>EU</th><th>BW</th><th>BY</th><th>BE</th>' +
            '<th>BB</th><th>HB</th><th>HH</th><th>HE</th><th>MV</th><th>NI</th><th>NW</th><th>RP</th><th>SL</th>' +
            '<th>SN</th><th>ST</th><th>SH</th><th>TH</th></tr></tfoot><tbody>']];

        }
        $('#opDE').prop("disabled", true);
        showLoadingAnimation(page = "DE");
        $.ajax({
            async: false,
            url: "/static/get_statisticsDE",
            dataType: "json",
            type: 'POST',
            data: {choiceTaxaDE: choiceTaxaDE, lang: lang},
            success: function (json) {
                if (choiceTaxaDE == "not_chosen_ta") {
                    $('#choose_taxon_first_warning_DE').removeClass('hidden');
                } else {
                    $('#choose_taxon_first_warning_DE').addClass('hidden');
                }
                dataDE = json.data;
                //Datatables
                $('#PromptArea').empty();
                $.each(json.data2, function (id, taxa) {
                    var EU = "", BW = "", BY = "", BE = "", BB = "", HB = "", HH = "", HE = "", MV = "", NI = "", NW = "",
                        RP = "", SL = "", SN = "", ST = "", SH = "", TH = "";
                    input = taxa[3];
                    input = input.toLowerCase();
                    if (input.match("europa")) {
                        EU = "+"
                    }
                    if (input.match("baden-württemberg")) {
                        BW = "+"
                    }
                    if (input.match("bayern")) {
                        BY = "+"
                    }
                    if (input.match("berlin")) {
                        BE = "+"
                    }
                    if (input.match("brandenburg")) {
                        BB = "+"
                    }
                    if (input.match("bremen")) {
                        HB = "+"
                    }
                    if (input.match("hamburg")) {
                        HH = "+"
                    }
                    if (input.match("hessen")) {
                        HE = "+"
                    }
                    if (input.match("mecklenburg-vorpommern")) {
                        MV = "+"
                    }
                    if (input.match("niedersachsen")) {
                        NI = "+"
                    }
                    if (input.match("nordrhein-westfalen")) {
                        NW = "+"
                    }
                    if (input.match("rheinland-pfalz")) {
                        RP = "+"
                    }
                    if (input.match("saarland")) {
                        SL = "+"
                    }
                    if (input.match("sachsen")) {
                        SN = "+"
                    }
                    if (input.match("sachsen-anhalt")) {
                        ST = "+"
                    }
                    if (input.match("schleswig-holstein")) {
                        SH = "+"
                    }
                    if (input.match("thüringen")) {
                        TH = "+"
                    }
                    table_data = '<tr><td>' + taxa[2] + '</td><td>' + EU + '</td><td>' + BW + '</td><td>' + BY + '</td><td>' + BE
                        + '</td><td>' + BB + '</td><td>' + HB + '</td><td>' + HH + '</td><td>' + HE + '</td><td>' +
                        MV + '</td><td>' + NI + '</td><td>' + NW + '</td><td>' + RP + '</td><td>' + SL + '</td><td>'
                        + SN + '</td><td>' + ST + '</td><td>' + SH + '</td><td>' + TH + '</td></tr>';
                    table_data_all_pivot.push(table_data);
                });
                table_data_all_pivot.push('</tbody></table>');
                $('#TableAreaDE').empty().append(table_data_all_pivot.join(' '));
                var taxon = $('#choiceTaxaDE').val();
                if (lang == 'de') {
                    language = {
                        "sEmptyTable": "Keine Daten in der Tabelle vorhanden",
                        "sInfo": "_START_ bis _END_ von _TOTAL_ Einträgen",
                        "sInfoEmpty": "0 bis 0 von 0 Einträgen",
                        "sInfoFiltered": "(gefiltert von _MAX_ Einträgen)",
                        "sInfoPostFix": "",
                        "sInfoThousands": ".",
                        "sLengthMenu": "_MENU_ Einträge anzeigen",
                        "sLoadingRecords": "Wird geladen...",
                        "sProcessing": "Bitte warten...",
                        "sSearch": "Suchen",
                        "sZeroRecords": "Keine Einträge vorhanden.",
                        "oPaginate": {
                            "sFirst": "Erste",
                            "sPrevious": "Zurück",
                            "sNext": "Nächste",
                            "sLast": "Letzte"
                        },
                        "oAria": {
                            "sSortAscending": ": aktivieren, um Spalte aufsteigend zu sortieren",
                            "sSortDescending": ": aktivieren, um Spalte absteigend zu sortieren"
                        }
                    }
                } else {
                    language = {}
                }
                $('#datatableDE').DataTable({
                    "bJQueryUI": true,
                    "language": language,
                    dom: 'T<"clear">lfrtip',
                    tableTools: {
                        "sSwfPath": "/static/js/DataTables/TableTools/swf/copy_csv_xls_pdf.swf",
                        "aButtons": [
                            "copy", {
                                "sExtends": "csv",
                                "sTitle": "Übersicht der in Deutschland gesammelten " + taxon
                            }, {
                                "sExtends": "pdf",
                                "sTitle": "Übersicht der in Deutschland gesammelten " + taxon
                            },
                            "print"
                        ]
                    }
                });
                hideLoadingAnimation(page = "DE");
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
                hideLoadingAnimation(page = "DE");
                $("#opDE").prop("disabled", false);
            }
        });
    };

    getValuesdrawPies = function (lang) {
        var div1, div2, div3 = '', count, l = 0, i = 0, choiceTaxaDE = $("#choiceTaxaDE_value").text(),
            taxon = $('#choiceTaxaDE').val();

        if (!lang) {
            lang = 'de';
        }

        ajaxDataRendererDE(lang, taxon);

        count = Object.keys(dataDE).length;

        if (choiceTaxaDE == "not_chosen_ta") {
            $('#TableAreaDE').empty()
        } else {
            if (count > 0) {
                if (taxon == "Alle Taxa") {
                    div1 = "<div id='chart";
                    div2 = "' class='chart left'></div>";
                } else {
                    div1 = "<div id='chart";
                    div2 = "' class='chart'></div>";
                }
                for (l; l < count; l++) {
                    div3 += div1 + l + div2;
                }
                $('#ChartArea').html(div3);

                $.each(dataDE, function (taxon, numbers) {
                    var total = 0;

                    $(numbers).map(function () {
                        total += this[1];
                    });

                    var myLabels = $.makeArray($(numbers).map(function () {
                        return this[0] + " " + Math.round(this[1] / total * 100) + "%";
                    }));

                    $('#chart' + i).jqplot([numbers], {
                        title: taxon,
                        seriesColors: ['#FF0000', '#FF8F35', '#008000'],
                        seriesDefaults: {
                            renderer: jQuery.jqplot.PieRenderer,
                            rendererOptions: {
                                showDataLabels: true,
                                highlightMouseOver: false,
                                dataLabels: myLabels,
                                sliceMargin: 3
                            }
                        },
                        grid: {
                            background: 'transparent',
                            drawGridlines: false,
                            borderColor: 'transparent',
                            shadow: false,
                            drawBorder: false,
                            shadowColor: 'transparent'
                        },
                        legend: {show: false, location: 'e'}
                    });
                    i++;
                });
            } else {
                $('#ChartArea').html('<div id="messageBox">Keine Daten vorhanden</div>');
            }
        }
    };

    /* ============ Statistics States ============== */

    ajaxDataRendererBL = function (lang) {
        var language,
            choiceTaxaBL = $('#choiceTaxaBL_value').text(),
            choiceStateBL = $("#choiceStateBL").val(),
            dataBL,
            taxon = $('#choiceTaxaBL').val(),
            bland = $("#choiceStateBL").children("option").filter(":selected").text(),
            table_data,
            table_data_all;
        if (lang == 'de') {
            table_data_all = [['<h2>&Uuml;bersicht der '] + taxon + [' in '] + bland +
            ['</h2><p>Die nicht gesammelten Arten beziehen sich auf die Taxonliste für ganz Deutschland. ' +
            'Dies bedeutet nicht automatisch, dass diese Art in diesem Bundesland vorkommt.</p>' +
            '<table id="datatableBL" class="display" cellspacing="0" width="100%"><thead><tr><th>Familie</th>' +
            '<th>Art</th><th>Anzahl gesammelt</th><th>Anzahl Barcodes</th></tr></thead><tfoot><tr><th>Familie</th>' +
            '<th>Art</th><th>Anzahl gesammelt</th><th>Anzahl Barcodes</th></tr></tfoot><tbody>']];
        } else {
            table_data_all = [['<h2>List of the '] + taxon + [' collected in '] + bland +
            ['</h2><p>"Not collected species" refers to the full taxon-list for Germany and does not ' +
            'necessarily mean that this particular species occurs in this federal state.</p>' +
            '<table id="datatableBL" class="display" cellspacing="0" width="100%"><thead><tr><th>Family</th>' +
            '<th>Species</th><th>Number collected</th><th>Number barcoded</th></tr></thead><tfoot><tr><th>Family</th>' +
            '<th>Species</th><th>Number collected</th><th>Number barcoded</th></tr></tfoot><tbody>']];
        }

        $("#opBL").prop("disabled", true);
        showLoadingAnimation(page = "BL");
        $.ajax({
            async: false,
            url: "/static/get_statisticsBL",
            dataType: "json",
            type: 'POST',
            data: {choiceTaxaBL: choiceTaxaBL, choiceStateBL: choiceStateBL},
            success: function (json) {
                dataBL = json.data;
                //Datatables
                if (choiceTaxaBL == "None" || choiceTaxaBL.slice(0, choiceTaxaBL.indexOf(";")) == "0") {
                    $('#choose_taxon_first_warning_BL').removeClass('hidden');
                } else {
                    $('#choose_taxon_first_warning_BL').addClass('hidden');
                    $.each(json.data2, function (id, taxa) {
                        table_data = '<tr><td>' + taxa[1] + '</td><td>' + taxa[2] + '</td><td>' + taxa[3] +
                            '</td><td>' + taxa[4] + '</td></tr>';
                        table_data_all.push(table_data);
                    });
                    $('#TableAreaBL').empty().append(table_data_all.join(' '));
                    var state = $('#choiceStateBL :selected').text();
                    var taxon = $('#choiceTaxaBL :selected').text();
                    if (lang == 'de') {
                        language = {
                            "sEmptyTable": "Keine Daten in der Tabelle vorhanden",
                            "sInfo": "_START_ bis _END_ von _TOTAL_ Einträgen",
                            "sInfoEmpty": "0 bis 0 von 0 Einträgen",
                            "sInfoFiltered": "(gefiltert von _MAX_ Einträgen)",
                            "sInfoPostFix": "",
                            "sInfoThousands": ".",
                            "sLengthMenu": "_MENU_ Einträge anzeigen",
                            "sLoadingRecords": "Wird geladen...",
                            "sProcessing": "Bitte warten...",
                            "sSearch": "Suchen",
                            "sZeroRecords": "Keine Einträge vorhanden.",
                            "oPaginate": {
                                "sFirst": "Erste",
                                "sPrevious": "Zurück",
                                "sNext": "Nächste",
                                "sLast": "Letzte"
                            },
                            "oAria": {
                                "sSortAscending": ": aktivieren, um Spalte aufsteigend zu sortieren",
                                "sSortDescending": ": aktivieren, um Spalte absteigend zu sortieren"
                            }
                        }
                    } else {
                            language = {}
                        }
                    $('#datatableBL').DataTable({
                        "bJQueryUI": true,
                        "language": language,
                        dom: 'T<"clear">lfrtip',
                        "order": [[2, "desc"]],
                        tableTools: {
                            "sSwfPath": "/static/js/DataTables/TableTools/swf/copy_csv_xls_pdf.swf",
                            "aButtons": [
                                "copy",
                                {
                                    "sExtends": "csv",
                                    "sTitle": "Übersicht der in " + state + " gesammelten " + taxon
                                },
                                {
                                    "sExtends": "pdf",
                                    "sTitle": "Übersicht der in " + state + " gesammelten " + taxon
                                },
                                "print"
                            ]
                        }
                    });
                }
                hideLoadingAnimation(page = "BL");
                $("#opBL").prop("disabled", false);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
                hideLoadingAnimation(page = "BL");
            }
        });
    };

    /* ============ Statistics Missing ============== */

    ajaxDataRendererMI = function (lang) {
        var language,
            choiceTaxaMI = $('#choiceTaxaMI_value').text(),
            dataMI,
            taxon = $('#choiceTaxaMI').val(),
            table_data,
            table_data_all;
        if (lang == 'de') {
            table_data_all = [['<h2>&Uuml;bersicht der fehlenden '] + taxon +
            ['</h2>' +
            '<table id="datatableMI" class="display" cellspacing="0" width="100%"><thead><tr><th>Familie</th>' +
            '<th>Art</th></tr></thead><tfoot><tr><th>Familie</th><th>Art</th></tr></tfoot><tbody>']];
        } else {
            table_data_all = [['<h2>List of the missing '] + taxon +
            ['</h2>' +
            '<table id="datatableMI" class="display" cellspacing="0" width="100%"><thead><tr><th>Family</th>' +
            '<th>Species</th></tr></thead><tfoot><tr><th>Family</th><th>Species</th></tr></tfoot><tbody>']];
        }

        $("#opMI").prop("disabled", true);
        showLoadingAnimation(page = "MI");
        $.ajax({
            async: false,
            url: "/static/get_statisticsMI",
            dataType: "json",
            type: 'POST',
            data: {choiceTaxaMI: choiceTaxaMI},
            success: function (json) {
                dataMI = json.data;
                //Datatables
                if (choiceTaxaMI == "not_chosen_taxa") {
                    $('#choose_taxon_first_warning_MI').removeClass('hidden');
                } else {
                    $('#choose_taxon_first_warning_MI').addClass('hidden');
                    $.each(json.data, function (id, taxa) {
                        table_data = '<tr><td>' + taxa[1] + '</td><td>' + taxa[2] + '</td></tr>';
                        table_data_all.push(table_data);
                    });
                    $('#TableAreaMI').empty().append(table_data_all.join(' '));
                    if (lang == 'de') {
                        language = {
                            "sEmptyTable": "Keine Daten in der Tabelle vorhanden",
                            "sInfo": "_START_ bis _END_ von _TOTAL_ Einträgen",
                            "sInfoEmpty": "0 bis 0 von 0 Einträgen",
                            "sInfoFiltered": "(gefiltert von _MAX_ Einträgen)",
                            "sInfoPostFix": "",
                            "sInfoThousands": ".",
                            "sLengthMenu": "_MENU_ Einträge anzeigen",
                            "sLoadingRecords": "Wird geladen...",
                            "sProcessing": "Bitte warten...",
                            "sSearch": "Suchen",
                            "sZeroRecords": "Keine Einträge vorhanden.",
                            "oPaginate": {
                                "sFirst": "Erste",
                                "sPrevious": "Zurück",
                                "sNext": "Nächste",
                                "sLast": "Letzte"
                            },
                            "oAria": {
                                "sSortAscending": ": aktivieren, um Spalte aufsteigend zu sortieren",
                                "sSortDescending": ": aktivieren, um Spalte absteigend zu sortieren"
                            }
                        }
                    } else {
                            language = {}
                        }
                    $('#datatableMI').DataTable({
                        "bJQueryUI": true,
                        dom: 'T<"clear">lfrtip',
                        language: language,
                        tableTools: {
                            "sSwfPath": "/static/js/DataTables/TableTools/swf/copy_csv_xls_pdf.swf",
                            "aButtons": [
                                "copy",
                                {
                                    "sExtends": "csv",
                                    "sTitle": "Übersicht der fehlenden " + taxon
                                },
                                {
                                    "sExtends": "pdf",
                                    "sTitle": "Übersicht der fehlenden " + taxon
                                },
                                "print"
                            ]
                        }
                    });
                }
                hideLoadingAnimation(page = "MI");
                $("#opMI").prop("disabled", false);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
                hideLoadingAnimation(page = "MI");
            }
        });
    }
})(jQuery);


