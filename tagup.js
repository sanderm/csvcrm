function Tagup()
{
	
};

// global configs:
Tagup.sortKey = "numexityear_up";
Tagup.filterAggregationLength = 6;

Tagup.generateHeaderTag = function(tagName, tagCount, tagDataName)
{
	var $tagItem = Tagup.createElementWithClasses("a", ["headerTag"]);
	$tagItem.href = "?tag=" + tagName;
	$tagItem.setAttribute("tagFilter", tagName);
	$tagItem.setAttribute("tagDataName", tagDataName);
	var tagClickFn = function(event)
	{
		event.preventDefault();
		Tagup.filterByTag(event.currentTarget.getAttribute("tagfilter"), event.currentTarget.getAttribute("tagDataName"));
	}
	
	$tagItem.addEventListener("click", tagClickFn, false);
	if(tagDataName.substr(0, 3) === "cur")
		$tagItem.innerHTML = Tagup.createCurrencyString(tagName) + " (" + tagCount + ")";
	else
		$tagItem.innerHTML = tagName.replace('_', ' ') + " (" + tagCount + ")";
	return $tagItem;
};

Tagup.moveFilterListItemAfterFavourite = function($filterListItem)
{
	// find last favorite item:
	var $filterListItemContainer = document.getElementsByClassName("filterListItemContainer")[0];
	var $favouriteElements = document.getElementsByClassName("isFavourite");
	if($favouriteElements.length > 0)
	{
		var $lastFavouriteElement = $favouriteElements[$favouriteElements.length - 1];
		$filterListItemContainer.insertBefore($filterListItem,$lastFavouriteElement.nextSibling);
	}
	else
	{
		$filterListItemContainer.insertBefore($filterListItem,$filterListItemContainer.firstChild);
	}
};

Tagup.favouriteFilterItem = function($eventTargetEl, url)
{
	var $favouriteStarEl = $eventTargetEl.getElementsByClassName("favouriteIcon")[0];
	//Tagup.moveFilterListItemAfterFavourite($eventTargetEl);
	if($eventTargetEl.className.indexOf("isFavourite") > -1)
	{
		$favouriteStarEl.classList.remove("fa-star");
		$eventTargetEl.classList.remove("isFavourite");
		$favouriteStarEl.classList.add("fa-star-o");
		if(this.storedFavouriteFilterItems.indexOf(url) > -1)
			this.storedFavouriteFilterItems.splice(this.storedFavouriteFilterItems.indexOf(url), 1);
	}
	else
	{
		$favouriteStarEl.classList.remove("fa-star-o");
		$eventTargetEl.classList.add("isFavourite");
		$favouriteStarEl.classList.add("fa-star");
		this.storedFavouriteFilterItems.push(url);
	}
	localStorage.setItem("favouriteFilterItems", JSON.stringify(this.storedFavouriteFilterItems));
};

Tagup.setSelectedTagStyling = function(filterValue)
{
	var $headerTags = document.getElementsByClassName('headerTag');
	for(var i = 0; i < $headerTags.length; i++)
	{
		if($headerTags[i].getAttribute("tagfilter") === filterValue)
			$headerTags[i].classList.add("selectedTag");
		else
			$headerTags[i].classList.remove("selectedTag");
	}
}

Tagup.filterByTag = function(filterValue, tagDataName)
{
	var $elements = document.getElementsByClassName("filterListItem");
	if(tagDataName.substr(0, 3) === "cur" || tagDataName.substr(0, 3) === "num") // filter by range
	{
		var $headerElement = document.querySelector('.headerTag[tagdataname="' + tagDataName + '"][tagfilter="' + filterValue + '"]');
		if(!$headerElement) // exact filter match does not exist
		{
			var $allFilterTags = document.querySelectorAll('.headerTag[tagdataname="' + tagDataName + '"]');
			// loop through tags, find the best matching one:
			for(var i = 0; i < $allFilterTags.length; i++)
			{
				if(parseInt(filterValue) <= parseInt($allFilterTags[i].getAttribute("tagfilter")))
				{
					$headerElement = $allFilterTags[i];
					filterValue = $headerElement.getAttribute("tagfilter");
					break;
				}
			}
		}
		var prevValue = parseInt($headerElement.previousSibling.getAttribute("tagfilter"));
		if(!prevValue)
			prevValue = 0;
		
		for(var i = 0; i < $elements.length; i++)
		{
			var rowTagValue = parseInt($elements[i].getAttribute(tagDataName));
		
			if(rowTagValue > parseInt(prevValue) && rowTagValue <= filterValue)
				$elements[i].style.display = "block";
			else
				$elements[i].style.display = "none";
		}
	}
	else // filter by exact value
	{
		for(var i = 0; i < $elements.length; i++)
		{
			var rowTagValue = $elements[i].getAttribute(tagDataName);
		
			if(rowTagValue === filterValue)
				$elements[i].style.display = "block";
			else
				$elements[i].style.display = "none";
		}
	}
	
	Tagup.setSelectedTagStyling(filterValue);
};

Tagup.createElementWithClasses = function(tagName, classList)
{
	var $el = document.createElement(tagName);
	for(var i = 0; i < classList.length; i++)
	{
		$el.classList.add(classList[i]);
	}
	
	return $el;
};

Tagup.createTagString = function(tagString)
{
	if(typeof tagString === "string")
		return tagString.charAt(0).toUpperCase() + tagString.replace(' ', '_').slice(1);
	else
		return tagString;
};

Tagup.loadFirebaseCompanies = function($companyList)
{
	var ref = new Firebase(Tagup.firebaseUrl);
	$companyList.classList.add("loadingCompanies");

	if(Tagup.sortKey)
	{
		var columnSortName = Tagup.sortKey.substring(0, Tagup.sortKey.length - 3);
		
		ref.orderByChild(columnSortName).once("value", function(snapshot) 
		{
			if(Tagup.sortKey.indexOf("_up") > -1)
				Tagup.dataLoaded(snapshot, $companyList, true) // reverse
			else
				Tagup.dataLoaded(snapshot, $companyList, false)
		});
	}
};

Tagup.dataLoaded = function(snapshot, $bigContainer, isReverse)
{
	$bigContainer.className = ""; // remove loadingCompanies class
	var tagContainerList = [];
	var tagNameList = [];
    var $itemList = Tagup.createElementWithClasses("div", ["filterListItemContainer"]);
	var tags = [];
	var tagsInitialized = false;
	var infoFields = [];
	var embedFieldName = "";
	// generate list of items
	
	var companyList = [];
	snapshot.forEach(function(snapshotItem) {
		companyList.push(snapshotItem.val());
    });
    if(isReverse)
    	companyList.reverse();
    
	for(var i = 0; i < companyList.length; i++)
	{
		// find number of tags + info elements:
		if(!tagsInitialized)
		{
			for(var j = 0; j < Object.keys(companyList[i]).length; j++)
			{
				if(Object.keys(companyList[i])[j].substring(0, 3) === "tag" || 
					Object.keys(companyList[i])[j].substring(0, 3) === "num" ||
					Object.keys(companyList[i])[j].substring(0, 3) === "cur")
				{
					tagContainerList.push(document.createElement("div"));
					tagNameList.push(Object.keys(companyList[i])[j]);
					tags.push({});
				}
				
				if(Object.keys(companyList[i])[j].substring(0, 4) === "text" && Object.keys(companyList[i])[j] !== "textname")
				{
					infoFields.push(Object.keys(companyList[i])[j]);
				}
				
				if(Object.keys(companyList[i])[j].substring(0, 5) === "embed")
				{
					embedFieldName = Object.keys(companyList[i])[j];
				}
			}
			tagsInitialized = true;
		} 

		var $itemListItem = Tagup.createElementWithClasses("div", ["filterListItem"]);
		
		// header
		var $itemListItemHeader = Tagup.createElementWithClasses("div", ["filterListItemHeader"]);
		var $itemNameWrapper = Tagup.createElementWithClasses("div", ["filterListItemNameWrapper"]);
		var $itemFavouriteIcon = Tagup.createElementWithClasses("i", ["fa", "favouriteIcon"]);
		
		// check if item is a favourite:
		var isFavourite = false; //this.storedFavouriteFilterItems.indexOf(companyList[i]["urlname"]) > -1;
		
		$itemNameWrapper.appendChild($itemFavouriteIcon);
		var $itemName = Tagup._generateConditionalAnchorTag("textname", companyList[i], true);
		$itemNameWrapper.appendChild($itemName);
		$itemListItemHeader.appendChild($itemNameWrapper);
		
		var $listItemTagContainer = Tagup.createElementWithClasses("div", ["listItemTagContainer"]);
		var tagsEncoded = [];
		for(var j = 0; j < tagContainerList.length; j++)
		{
			tagsEncoded.push(Tagup.createTagString(companyList[i][tagNameList[j]]));
			var $tag = this.createTagElement(companyList[i][tagNameList[j]], tagsEncoded[j], tagNameList[j]);
			$listItemTagContainer.appendChild($tag);
		}

		$itemListItemHeader.appendChild($listItemTagContainer);
		
		// innerEl
		var $itemListInnerEl = Tagup.createElementWithClasses("div", ["filterListItemInner"]);
		
		for(var j = 0; j < infoFields.length; j++)
		{
			var $itemInfoEl = Tagup._generateConditionalAnchorTag(infoFields[j], companyList[i], true)
			$itemListInnerEl.appendChild($itemInfoEl);
		}
		
		if(companyList[i]["description"])
		{
			var $itemDescription = document.createElement("span");
			$itemDescription.innerHTML = companyList[i]["description"];
			$itemListInnerEl.appendChild($itemDescription);
			// $itemListInnerEl.style.display = "none";
		}
		
		var toggleInfoSectionFn = function(event)
		{
			var $eventTargetEl = event.target;
			if($eventTargetEl.className.indexOf("favouriteIcon") > -1)
			{
				var url = event.currentTarget.getElementsByClassName("filterListItemName")[0].href;
				Tagup.favouriteFilterItem(event.currentTarget.parentElement, url);
			}
			else if($eventTargetEl.tagName !== 'A')
			{
				event.preventDefault();
				var $filterListItemEl = event.currentTarget.parentElement;
				var $filterListItemInner = $filterListItemEl.getElementsByClassName("filterListItemInner")[0];
				if ($filterListItemInner.style.display === "block")
				{
					$filterListItemInner.style.display = "none";
					$filterListItemEl.classList.remove("open");	
				}
				else
				{
					$filterListItemInner.style.display = "block";
					$filterListItemEl.classList.add("open");	
				}
			}
			else if($eventTargetEl.className.indexOf("filterListItemTag") > -1)
			{
				event.preventDefault();
				Tagup.filterByTag($eventTargetEl.getAttribute("tagfilter"), $eventTargetEl.getAttribute("tagDataName"));
			}
		}
		$itemListItemHeader.addEventListener("click", toggleInfoSectionFn, false);
		
		$itemListItem.appendChild($itemListItemHeader);
		$itemListItem.appendChild($itemListInnerEl);
		if (companyList[i][embedFieldName])
		{
			var $embedElement = Tagup._generateEmbedElement(companyList[i][embedFieldName]);
			$itemListItem.appendChild($embedElement);
		}
		$itemList.appendChild($itemListItem);
	
		if(isFavourite)
		{
			//Tagup.moveFilterListItemAfterFavourite($itemListItem);
			$itemFavouriteIcon.classList.add("fa-star");
			$itemListItem.classList.add("isFavourite");
		}
		else
		{
			$itemFavouriteIcon.classList.add("fa-star-o");
		}
		
		for(var j = 0; j < tagsEncoded.length; j++)
		{
			if (tags[j].hasOwnProperty(tagsEncoded[j]))
				tags[j][tagsEncoded[j]] += 1;	
			else
				tags[j][tagsEncoded[j]] = 1;
			
			$itemListItem.setAttribute(tagNameList[j], tagsEncoded[j]);
		}
	}
		
	var tagShowAllClickFn = function(event)
	{
		event.preventDefault();
		var $elements = document.getElementsByClassName("filterListItem");
		for(var i = 0; i < $elements.length; i++)
		{
			$elements[i].style.display = "block";
		}
		
		Tagup.setSelectedTagStyling("");
	}
	
	// generate all header tags
	for (var j = 0; j < tags.length; j++)
	{
		var $tagShowAllTag = Tagup.createElementWithClasses("a", ["showAllTags"]);
		$tagShowAllTag.innerHTML = tagNameList[j].substring(3) + " (" + companyList.length + ")";
		$tagShowAllTag.href = "";
		$tagShowAllTag.addEventListener("click", tagShowAllClickFn, false);
		tagContainerList[j].appendChild($tagShowAllTag);
		
		var tagsCopy = tags.slice();
		// generate range tags: 
		
		if(Object.keys(tagsCopy[j]).length > Tagup.filterAggregationLength)
		{
			tagsCopy[j] = Tagup._generateAggregatedTagList(tagsCopy[j]);
		}
		
		for (var key in tagsCopy[j])
		{
			var tagCount = tagsCopy[j][key];
			if(tagCount > 0)
			{
				var $tagItem = Tagup.generateHeaderTag(key, tagCount, tagNameList[j]);
				tagContainerList[j].appendChild($tagItem);	
			}
		}
		
		$bigContainer.appendChild(tagContainerList[j]);
	}
		
	var $sortContainer = Tagup.createElementWithClasses("div", ["sortContainer"]);
	
	// add sort by name:
	var $sortNameTag = Tagup._generateSortButton("name", "Name", ["sortNameTag"]);
	$sortContainer.appendChild($sortNameTag);
	
	// generate tag sort arrows:
	var $tagSortContainer = Tagup.createElementWithClasses("div", ["tagSortContainer"]);
	for (var j = 0; j < tagNameList.length; j++)
	{
		var $sortTag = Tagup._generateSortButton(tagNameList[j], tagNameList[j].substring(3), []);
		$tagSortContainer.appendChild($sortTag);
	}
	$sortContainer.appendChild($tagSortContainer);
	
	// add sort by info data fields:
	for(var j = 0; j < infoFields.length; j++)
	{
		var $sortInfoFieldTag = Tagup._generateSortButton(infoFields[j], infoFields[j].substring(4), ["sortInfoFieldTag"]);
		$sortContainer.appendChild($sortInfoFieldTag);
	}
	
	// add sort by description:
	var $sortDescriptionTag = Tagup._generateSortButton("description", "Description", ["sortDescriptionTag"]);
	$sortContainer.appendChild($sortDescriptionTag);
	
	$bigContainer.appendChild($sortContainer);
	$bigContainer.appendChild($itemList);
};

Tagup._generateEmbedElement = function(embedFieldValue)
{
	var re = /(?:\.([^.]+))?$/;
	var $embedElement = Tagup.createElementWithClasses("div", ["embedElement"]);
	
	if(embedFieldValue.substr(0, 4) !== "http")
	{
		$embedElement.innerHTML = 'Embed link does not start with http. Please add http:// or https:// to embed link'
	}
	// check for file extension. Then it is an image:
	else if (re.exec(embedFieldValue)[1] === "jpg" || 
		re.exec(embedFieldValue)[1] === "jpeg" ||
		re.exec(embedFieldValue)[1] === "png")
	{
		var $embedImage = Tagup.createElementWithClasses("img", []);
		$embedImage.setAttribute("src", embedFieldValue);
		$embedElement.appendChild($embedImage);
	}
	else // else embed as iframe:
	{
		$embedElement.innerHTML = '<iframe width="560" height="325" src="'+ embedFieldValue + '"></iframe>';
	}
	
	return $embedElement;
};

Tagup._generateConditionalAnchorTag = function(infoFieldName, companyData, useFavIcons)
{
	var infoUrl = companyData["url" + infoFieldName.substr(4, infoFieldName.length)];
	var $itemInfoWrapper = Tagup.createElementWithClasses("div", ["itemInfoWrapper"]);
	var $itemInfoEl;
	if(infoUrl && infoUrl.substr(0, 4) === "http")
	{
		$itemInfoEl = Tagup.createElementWithClasses("a", ["itemInfo"]);
		$itemInfoEl.href = infoUrl;
		
		if(useFavIcons)
		{
			var $iconEl = Tagup.createElementWithClasses("img", ["faviconImage"]);
			$iconEl.setAttribute("src", "https://www.google.com/s2/favicons?domain=" + infoUrl);
			$itemInfoWrapper.appendChild($iconEl);
			$itemInfoWrapper.appendChild($itemInfoEl);	
		}
	}
	else
	{
		$itemInfoEl = Tagup.createElementWithClasses("span", ["itemInfo"]);
		$itemInfoWrapper.appendChild($itemInfoEl);
	}
	$itemInfoEl.innerHTML = companyData[infoFieldName];
	return $itemInfoWrapper;
};

Tagup._generateSortButton = function(sortColumnName, sortColumnNameText, extraClasses)
{
	var $sortTagOuter = Tagup.createElementWithClasses("div", ["sortTagOuter"].concat(extraClasses));
	var $sortTag = Tagup.createElementWithClasses("div", ["sortTag"]);
	var $sortTagName = Tagup.createElementWithClasses("span", []); 
	var $sortTagArrow = Tagup.createElementWithClasses("div", ["fa"]); 
	$sortTagName.innerHTML = sortColumnNameText;

	if(Tagup.sortKey.indexOf(sortColumnName) > -1)
	{
		if(Tagup.sortKey.indexOf("_up") > -1)
		{
			$sortTag.setAttribute("sortKey", sortColumnName + "_dn");
			$sortTagArrow.classList.add("fa-caret-down");
		}
		else
		{
			$sortTag.setAttribute("sortKey", sortColumnName + "_up");
			$sortTagArrow.classList.add("fa-caret-up");
		}
	}
	else
	{
		$sortTag.setAttribute("sortKey", sortColumnName + "_up");
		$sortTagArrow.classList.add("fa-caret-up");
	}
	
	$sortTag.appendChild($sortTagName);
	$sortTag.appendChild($sortTagArrow);
	var tagSortFn = function(event)
	{
		event.preventDefault();
		Tagup.sortKey = event.currentTarget.getAttribute("sortKey");
		var $companyList = document.getElementById("companyList");
		
		// clear all content...
		$companyList.innerHTML = "";
		Tagup.loadFirebaseCompanies($companyList);
	}
	$sortTag.addEventListener("click", tagSortFn, false);
	
	$sortTagOuter.appendChild($sortTag);
	return $sortTagOuter;
};

Tagup._generateAggregatedTagList = function(originalTagList)
{
	// find lowest and highest values:
	var lowest = parseInt(Object.keys(originalTagList)[0]);
	var highest = parseInt(Object.keys(originalTagList)[0]);
	for(var k = 1; k < Object.keys(originalTagList).length; k++)
	{
		var valueToEvaluate = parseInt(Object.keys(originalTagList)[k]);
		if(valueToEvaluate < lowest)
			lowest = valueToEvaluate;
		if(valueToEvaluate > highest)
			highest = valueToEvaluate;
	}
	
	var finalDict = {};
	finalDict[Math.ceil(lowest)] = 0;
	finalDict[Math.ceil(lowest + (highest - lowest) * 0.125)] = 0;
	finalDict[Math.ceil(lowest + (highest - lowest) * 0.250)] = 0;
	finalDict[Math.ceil(lowest + (highest - lowest) * 0.375)] = 0;
	finalDict[Math.ceil(lowest + (highest - lowest) * 0.500)] = 0;
	finalDict[Math.ceil(lowest + (highest - lowest) * 0.625)] = 0;
	finalDict[Math.ceil(lowest + (highest - lowest) * 0.750)] = 0;
	finalDict[Math.ceil(lowest + (highest - lowest) * 0.875)] = 0;
	finalDict[Math.ceil(highest)] = 0;
	
	var sortedFinalKeys = [];
	for(var key in finalDict)
	{
		sortedFinalKeys.push(parseInt(key));
	}
	sortedFinalKeys.sort(function (a, b) { return a > b });
	
	// find how many companies are in each segment
	for(var key in originalTagList)
	{
		for(var i = 0; i < sortedFinalKeys.length; i++)
		{
			if(parseInt(key) <= sortedFinalKeys[i])
			{
				finalDict[sortedFinalKeys[i]] += originalTagList[key];
				break;
			}
		}
		/*
		if(parseInt(key) <= sortedFinalKeys[0])
			finalDict[sortedFinalKeys[0]] += originalTagList[key];
		else if(parseInt(key) <= sortedFinalKeys[1])
			finalDict[sortedFinalKeys[1]] += originalTagList[key];
		else if(parseInt(key) <= sortedFinalKeys[2])
			finalDict[sortedFinalKeys[2]] += originalTagList[key];
		else if(parseInt(key) <= sortedFinalKeys[3])
			finalDict[sortedFinalKeys[3]] += originalTagList[key];
		else if(parseInt(key) <= sortedFinalKeys[4])
			finalDict[sortedFinalKeys[4]] += originalTagList[key];
		*/
	}
	
	return finalDict;
};

Tagup.createTagElement = function(tagDisplayLabel, tagEncodedValue, tagHeaderName)
{
	var $tag = Tagup.createElementWithClasses("a", ["filterListItemTag"]);
	$tag.href = "?tag=" + tagEncodedValue;
	$tag.setAttribute("tagFilter", tagEncodedValue);
	$tag.setAttribute("tagDataName", tagHeaderName);
	if(tagHeaderName)
	if(tagHeaderName.substr(0, 3) === "cur") // currency tag value
		$tag.innerHTML = Tagup.createCurrencyString(tagDisplayLabel);
	else
		$tag.innerHTML = tagDisplayLabel;
	return $tag;
};

Tagup.createCurrencyString = function(value)
{
	return "$" + value + "M";
};

Tagup.createEcosystemImage = function(imagePath)
{
	var $ecosystemImageLink = document.createElement("a");
	$ecosystemImageLink.href = "startupmap.rev25-normal.png";
	$ecosystemImageLink.innerHTML = '<img class="alignnone size-medium wp-image-161212" alt="startupmap.rev25-normal" src="' + imagePath + '" width="940" height="648">'

	var $maindiv = Tagup.createElementWithClasses("div", ["maindiv"]);
	$maindiv.appendChild($ecosystemImageLink);
	return $maindiv;
};

Tagup.initialize = function(firebaseUrl, imagePath, parentElement)
{
	Tagup.firebaseUrl = firebaseUrl;
	this.storedFavouriteFilterItems = localStorage.hasOwnProperty("favouriteFilterItems") ? JSON.parse(localStorage.getItem("favouriteFilterItems")) : [];

	var $companyList = document.createElement("div");
	$companyList.id = "companyList";
	Tagup.loadFirebaseCompanies($companyList);
	var $ecosystemImage = Tagup.createEcosystemImage(imagePath);
	
	var $parentTag;
	if(!parentElement)
	{
		var $scriptTag = document.scripts[document.scripts.length - 1];
    	var $parentTag = $scriptTag.parentNode;
	}
	else
	{
		$parentTag = parentElement;
	}
	
	$parentTag.appendChild($ecosystemImage);
	$parentTag.appendChild($companyList);
	
	var filePicker = document.createElement("INPUT");
	filePicker.setAttribute("type", "file");
	filePicker.setAttribute("id", "txtFileUpload");
	filePicker.setAttribute("accept", ".csv");
	filePicker.addEventListener('change', Tagup.readCsvFile, false);
	document.getElementsByTagName("body")[0].appendChild(filePicker);
	
	var $signoutButton = document.createElement("button");
	$signoutButton.innerHTML = "sign out of firebase";
	var signoutFn = function(event)
	{
		new Firebase(Tagup.firebaseUrl).auth().signOut().then(function() {
			console.log("sign out success");
		}, function(error) {
			console.log("sign out failed");
		});
	}

	$signoutButton.addEventListener("click", signoutFn, false);
	document.getElementsByTagName("body")[0].appendChild($signoutButton);
};


Tagup.readCsvFile = function(evt)
{
	var file = evt.target.files[0];
	var formData = new FormData();
	formData.append('csvfile', file, file.name);
	
	var xhr = new XMLHttpRequest();
	xhr.open('POST', 'https://swapp-sanderm1.c9users.io/upload', true);
	xhr.send(formData);
	/*
	var data = null;
    var file = evt.target.files[0];
    var reader = new FileReader();
    reader.readAsText(file);
    
    reader.onload = function(event) 
    {
    	var csvData = event.target.result;
        data = $.csv.toObjects(csvData);
        //console.log(data);
        
        var ref = new Firebase(Tagup.firebaseUrl);
        ref.set(data, function()
        {
        	window.location.reload(true);
        });
        
    };
    */
};

Tagup.removeAllFirebaseData = function()
{
	var ref = new Firebase(Tagup.firebaseUrl);
	
	var onComplete = function(error) 
	{
		if (error) {
    		console.log('Synchronization failed');
		} else {
    		console.log('Synchronization succeeded');
		}
	};
	ref.remove(onComplete);
};