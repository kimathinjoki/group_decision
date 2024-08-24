// function grpDecision() {
//   var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
//   var range = sheet.getDataRange();
//   var data = range.getValues();

//   // Extract headers (first row) and data excluding the first column (which contains strings)
//   var candidates = [];

//   for (var i = 1; i < data.length; i++) {
//     var rowData = data[i].slice(1); // Skip the first column (participant names)
//     candidates.push(rowData);
//   }

//   // Prepare the payload
//   var payload = {
//     'data': candidates
//   };

//   Logger.log(JSON.stringify(payload)); // Log payload for debugging

//   var options = {
//     'method': 'post',
//     'contentType': 'application/json',
//     'payload': JSON.stringify(payload),
//     'muteHttpExceptions': true
//   };

//   // script url
//   var url = "https://grpdecisionvercel-kimathinjokis-projects.vercel.app/group_decision";

//   // var url = "https://us-central1-loyal-karma-433415-t7.cloudfunctions.net/vanilla_cct";

//   // var url = "https://vanilla-cct.onrender.com/consensus";

//   try {
    
//     var response = UrlFetchApp.fetch(url, options);
//     Logger.log('Response Code: ' + response.getResponseCode());
//     Logger.log('Response Content: ' + response.getContentText());
//     var consensusResult = JSON.parse(response.getContentText());
    
//     // Insert the "Consensus" row after the last row of data
//     var lastRow = sheet.getLastRow() + 1;
//     sheet.getRange(lastRow, 1).setValue("Consensus");

//     // Populate the consensus values starting from the second column
//     sheet.getRange(lastRow, 2, 1, consensusResult.length).setValues([consensusResult]);
//   } catch (error) {
//     Logger.log('Error: ' + error.message);
//   }
// }

// function grpDecision() {
//   var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
//   var range = sheet.getDataRange();
//   var data = range.getValues();

//   // Headers row
//   var headers = data[0];

//   // Skip the first column and process the rest
//   var candidates = {};

//   for (var i = 1; i < headers.length; i++) { // Start from 1 to skip the first column
//     var columnData = [];
//     for (var j = 1; j < data.length; j++) { // Skip the header row
//       columnData.push(data[j][i]);
//     }
//     candidates[headers[i]] = columnData;
//   }

//   var url = "https://vanilla-cct.onrender.com/consensus";

//   var options = {
//     'method': 'post',
//     'contentType': 'application/json',
//     'payload': JSON.stringify(candidates)
//   };

//   var response = UrlFetchApp.fetch(url, options);
//   var averages = JSON.parse(response.getContentText()).consensus;

//   // Add a "Consensus" label in the first column after the last data row
//   var consensusRow = data.length + 1;
//   sheet.getRange(consensusRow, 1).setValue("Consensus");

//   // Populate the calculated consensus in the corresponding columns, starting from column 2
//   for (var i = 1; i < headers.length; i++) { // Start from 1 to match the skipped first column
//     var header = headers[i];
//     if (averages[i - 1] !== undefined) { // Adjust index to match the consensus array
//       sheet.getRange(consensusRow, i + 1).setValue(averages[i - 1]);
//     }
//   }
// }

// function grpDecision() {
//   var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet()
//   var range = sheet.getDataRange()
//   var data = range.getValues()

//   // headers row
//   var headers = data[0]

//   var candidates = {}

//   for (var i = 0; i < headers.length; i++) {
//     var columnData = [];
//     for (var j = 1; j < data.length; j++) {
//       columnData.push(data[j][i]);
//     }
//     candidates[headers[i]] = columnData;
//   }

//   // render deployed link
//   // var url = "https://group-decision-6i3i.onrender.com/group_decision" 

//   // vercel deployed link
//   // var  url = "https://grpdecisionvercel-nrgc535uh-kimathinjokis-projects.vercel.app/group_decision"

//   // google cloud function
//   // var url = "https://us-central1-loyal-karma-433415-t7.cloudfunctions.net/cct-v3"

//   var options = {
//     'method': 'post',
//     'contentType': 'application/json',
//     'payload': JSON.stringify(candidates) 
//   }

//   var response = UrlFetchApp.fetch(url, options)
//   var averages = JSON.parse(response.getContentText()); 

//   var lastRow = data.length + 1
//   for(var i = 0; i < headers.length; i++) {
//     var header = headers[i]
//     if(averages[header] !== undefined) {
//       sheet.getRange(lastRow, i +1).setValue(averages[header])
//     }
//   }

// }

function grpDecision() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var range = sheet.getDataRange();
  var data = range.getValues();

  // Headers row
  var headers = data[0];

  // Skip the first column and process the rest
  var candidates = {};

  for (var i = 1; i < headers.length; i++) { // Start from 1 to skip the first column
    var columnData = [];
    for (var j = 1; j < data.length; j++) { // Skip the header row
      columnData.push(data[j][i]);
    }
    candidates[headers[i]] = columnData;
  }

  // script url
  var url = "https://grpdecisionvercel-kimathinjokis-projects.vercel.app/group_decision";

  //  google cloud run script url

  // var url = "https://us-central1-loyal-karma-433415-t7.cloudfunctions.net/vanilla_cct";

  var options = {
    'method': 'post',
    'contentType': 'application/json',
    'payload': JSON.stringify(candidates)
  };

  var response = UrlFetchApp.fetch(url, options);
  var averages = JSON.parse(response.getContentText());

  // Add a "Consensus" label in the first column after the last data row
  var consensusRow = data.length + 1;
  sheet.getRange(consensusRow, 1).setValue("Consensus");

  // Populate the calculated consensus in the corresponding columns, starting from column 2
  for (var i = 1; i < headers.length; i++) { // Start from 1 to match the skipped first column
    var header = headers[i];
    if (averages[header] !== undefined) {
      sheet.getRange(consensusRow, i + 1).setValue(averages[header]);
    }
  }
}




function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Cct Tools')
  .addItem('Calc Canditate Mean', 'grpDecision')
  .addToUi()
}