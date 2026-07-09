// ── TWO FOLDER IDs TO SET ──
var GALLERY_FOLDER_ID  = '17ygm-JDfNcukJnCnyABcG5F7bDq3I35O';
var FEATURED_FOLDER_ID = '1tjgi4Z-pWf6wGFyqPQmjD4RAZc02xigv';
var API_KEY = 'AIzaSyCHwTX1HZ5__W72yXptl6YCvjVXn5k1aBI';

// ── EMAIL ROUTING ──
// Quote form notifications (Shane, Kevin, and developer)
var QUOTE_EMAILS = [
  'slochan@slinstallations.ca',
  'kevin@slinstallations.ca',
  'ahmed.rehman@gmail.com'
];
// Feedback/update form notifications (developer only)
var UPDATE_EMAILS = [
  'ahmed.rehman@gmail.com'
];

function doPost(e) {
  try {
    var d = JSON.parse(e.postData.contents);

    // ── WEBSITE UPDATE REQUESTS → developer only
    if (d.formType === 'websiteUpdate') {
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var updateSheet = ss.getSheetByName('Updates') || ss.insertSheet('Updates');
      if (updateSheet.getLastRow() === 0) {
        updateSheet.appendRow(['Timestamp','Name','Email','Update Type','Page','Details','Links']);
      }
      updateSheet.appendRow([
        new Date().toLocaleString('en-CA'),
        d.name, d.email, d.updateType, d.page, d.details, d.links
      ]);

      var devHtml =
        '<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;background:#f5f5f5;padding:20px">' +
          '<div style="background:#fff;border-radius:4px;overflow:hidden">' +
            '<div style="background:#0d0d0d;padding:24px 32px;text-align:center">' +
              '<div style="color:#fff;font-family:Arial,sans-serif;font-size:20px;font-weight:700;letter-spacing:1px">SL INSTALLATIONS & SOLUTIONS</div>' +
            '</div>' +
            '<div style="background:#D10000;padding:14px 32px">' +
              '<span style="color:#fff;font-size:16px;font-weight:700;letter-spacing:1px">📝 WEBSITE UPDATE REQUEST</span>' +
            '</div>' +
            '<div style="padding:24px 32px">' +
              '<table style="width:100%;border-collapse:collapse">' +
                '<tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">From</span><br><span style="font-size:15px;color:#333">' + d.name + ' &lt;' + d.email + '&gt;</span></td></tr>' +
                '<tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Type of Update</span><br><span style="font-size:15px;color:#333">' + d.updateType + '</span></td></tr>' +
                '<tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Page</span><br><span style="font-size:15px;color:#333">' + d.page + '</span></td></tr>' +
                '<tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Details</span><br><span style="font-size:15px;color:#333">' + d.details + '</span></td></tr>' +
                (d.links ? '<tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Links / References</span><br><span style="font-size:15px;color:#333">' + d.links + '</span></td></tr>' : '') +
              '</table>' +
            '</div>' +
            '<div style="background:#f5f5f5;padding:16px 32px;text-align:center;border-top:1px solid #eee">' +
              '<span style="font-size:12px;color:#999">Submitted via SL Update Form | ' + new Date().toLocaleString('en-CA') + '</span>' +
            '</div>' +
          '</div>' +
        '</div>';

      UPDATE_EMAILS.forEach(function(email) {
        MailApp.sendEmail(email, '📝 Website Update — SL Installations — ' + d.updateType, '', {htmlBody: devHtml, name: 'SL Update Form'});
      });

      var clientConfirmHtml =
        '<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;background:#f5f5f5;padding:20px">' +
          '<div style="background:#fff;border-radius:4px;overflow:hidden">' +
            '<div style="background:#0d0d0d;padding:24px 32px;text-align:center">' +
              '<div style="color:#fff;font-family:Arial,sans-serif;font-size:20px;font-weight:700;letter-spacing:1px">SL INSTALLATIONS & SOLUTIONS</div>' +
            '</div>' +
            '<div style="background:#D10000;padding:14px 32px">' +
              '<span style="color:#fff;font-size:16px;font-weight:700;letter-spacing:1px">✅ UPDATE REQUEST RECEIVED</span>' +
            '</div>' +
            '<div style="padding:32px">' +
              '<p style="font-size:16px;color:#0d0d0d;margin:0 0 16px">Hi ' + d.name + ',</p>' +
              '<p style="font-size:15px;color:#444;line-height:1.6;margin:0 0 16px">We have received your website update request and will action it within <strong>3 to 5 business days</strong>.</p>' +
              '<p style="font-size:13px;color:#888;margin:0">If you have any questions, reply to this email.</p>' +
            '</div>' +
            '<div style="background:#0d0d0d;padding:16px 32px;text-align:center">' +
              '<span style="font-size:12px;color:rgba(255,255,255,.5)">SL Installations & Solutions Inc. | slinstallations.ca</span>' +
            '</div>' +
          '</div>' +
        '</div>';

      MailApp.sendEmail(d.email, 'Update Request Received — SL Installations & Solutions', '', {htmlBody: clientConfirmHtml, name: 'SL Installations & Solutions'});
      return ContentService.createTextOutput(JSON.stringify({status:'ok'})).setMimeType(ContentService.MimeType.JSON);
    }

    // ── QUOTE FORM
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    if (sheet.getLastRow()===0) sheet.appendRow(['Timestamp','Name','Company','Email','Phone','Type','Brands','Workstations','Location','Target Date','Notes','Floor Plan']);
    var fpLink = '';
    if (d.floorPlan) {
      var bytes = Utilities.base64Decode(d.floorPlan);
      var blob  = Utilities.newBlob(bytes, d.floorPlanType, d.floorPlanName);
      var file  = DriveApp.createFile(blob);
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
      fpLink = file.getUrl();
    }
    sheet.appendRow([new Date().toLocaleString('en-CA'),d.name,d.company,d.email,d.phone,d.projectType,d.brands,d.workstations,d.location,d.targetDate,d.notes,fpLink]);

    var clientHtml =
      '<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;background:#f5f5f5;padding:20px"><div style="background:#fff;border-radius:4px;overflow:hidden"><div style="background:#0d0d0d;padding:24px 32px;text-align:center"><img src="https://cpggrowthstudio.github.io/sl-installations/logo.png" alt="SL Installations" style="height:56px" onerror="this.style.display=\'none\'"><div style="color:#fff;font-size:20px;font-weight:700;margin-top:8px;letter-spacing:1px">SL INSTALLATIONS & SOLUTIONS</div></div><div style="background:#D10000;padding:14px 32px"><span style="color:#fff;font-size:16px;font-weight:700;letter-spacing:1px">✅ REQUEST RECEIVED</span></div><div style="padding:32px"><p style="font-size:16px;color:#0d0d0d;margin:0 0 16px">Hi '+d.name+',</p><p style="font-size:15px;color:#444;line-height:1.6;margin:0 0 16px">Thank you for reaching out. We have received your project request and a member of our team will be in touch within <strong>24 business hours</strong>.</p><p style="font-size:15px;color:#444;line-height:1.6;margin:0 0 24px">If you need to reach us sooner:</p><table style="width:100%;border-collapse:collapse;margin-bottom:24px"><tr><td style="padding:12px 16px;background:#f9f9f9;border-left:3px solid #D10000"><div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888;margin-bottom:4px">Shane Lochan — Director</div><div style="font-size:15px;color:#0d0d0d;font-weight:600">647.504.3169 | slochan@slinstallations.ca</div></td></tr><tr><td style="padding:4px"></td></tr><tr><td style="padding:12px 16px;background:#f9f9f9;border-left:3px solid #D10000"><div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888;margin-bottom:4px">Kevin Ramnath — Operations Manager</div><div style="font-size:15px;color:#0d0d0d;font-weight:600">647.992.8500 | kevin@slinstallations.ca</div></td></tr></table><p style="font-size:13px;color:#888;margin:0">Ontario\'s commercial furniture installation specialists.</p></div><div style="background:#0d0d0d;padding:16px 32px;text-align:center"><span style="font-size:12px;color:rgba(255,255,255,.5)">SL Installations & Solutions Inc. | slinstallations.ca</span></div></div></div>';

    MailApp.sendEmail(d.email, 'Your Request — SL Installations & Solutions', '', {htmlBody: clientHtml, name: 'SL Installations & Solutions'});

    var fpRow = fpLink ? '<tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Floor Plan</span><br><a href="'+fpLink+'" style="color:#D10000;font-weight:600">View Uploaded Floor Plan</a></td></tr>' : '';

    var htmlBody =
      '<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;background:#f5f5f5;padding:20px"><div style="background:#fff;border-radius:4px;overflow:hidden"><div style="background:#0d0d0d;padding:24px 32px;text-align:center"><img src="https://cpggrowthstudio.github.io/sl-installations/logo.png" alt="SL Installations" style="height:56px" onerror="this.style.display=\'none\'"><div style="color:#fff;font-size:20px;font-weight:700;margin-top:8px;letter-spacing:1px">SL INSTALLATIONS & SOLUTIONS</div></div><div style="background:#D10000;padding:14px 32px"><span style="color:#fff;font-size:16px;font-weight:700;letter-spacing:1px">📋 NEW QUOTE REQUEST</span></div><div style="padding:24px 32px"><table style="width:100%;border-collapse:collapse"><tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Name</span><br><span style="font-size:15px;color:#333">'+d.name+'</span></td></tr><tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Company</span><br><span style="font-size:15px;color:#333">'+d.company+'</span></td></tr><tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Email</span><br><span style="font-size:15px;color:#333">'+d.email+'</span></td></tr><tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Phone</span><br><span style="font-size:15px;color:#333">'+d.phone+'</span></td></tr><tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Project Type</span><br><span style="font-size:15px;color:#333">'+d.projectType+'</span></td></tr><tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Brands</span><br><span style="font-size:15px;color:#333">'+d.brands+'</span></td></tr><tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Workstations</span><br><span style="font-size:15px;color:#333">'+d.workstations+'</span></td></tr><tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Location</span><br><span style="font-size:15px;color:#333">'+d.location+'</span></td></tr><tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Target Date</span><br><span style="font-size:15px;color:#333">'+d.targetDate+'</span></td></tr><tr><td style="padding:10px 0;border-bottom:1px solid #eee"><span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888">Notes</span><br><span style="font-size:15px;color:#333">'+d.notes+'</span></td></tr>'+fpRow+'</table></div><div style="background:#f5f5f5;padding:16px 32px;text-align:center;border-top:1px solid #eee"><span style="font-size:12px;color:#999">Submitted via slinstallations.ca | '+new Date().toLocaleString('en-CA')+'</span></div></div></div>';

    QUOTE_EMAILS.forEach(function(email) {
      MailApp.sendEmail(email, '📋 New Quote — '+d.name, '', {htmlBody: htmlBody, name: 'SL Installations Website'});
    });

    return ContentService.createTextOutput(JSON.stringify({status:'ok'})).setMimeType(ContentService.MimeType.JSON);
  } catch(err) {
    Logger.log('ERROR: ' + err.toString());
    return ContentService.createTextOutput(JSON.stringify({status:'error',message:err.toString()})).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  try {
    var action = (e && e.parameter && e.parameter.action) ? e.parameter.action : '';
    if (action === 'featured') {
      var folder = DriveApp.getFolderById(FEATURED_FOLDER_ID);
      var files = folder.getFiles();
      var photos = [];
      while (files.hasNext() && photos.length < 4) {
        var f = files.next();
        if (f.getMimeType().indexOf('image') === -1) continue;
        photos.push({name: f.getName(), url: 'https://drive.google.com/uc?export=view&id=' + f.getId()});
      }
      return ContentService.createTextOutput(JSON.stringify(photos)).setMimeType(ContentService.MimeType.JSON);
    }
    if (action === 'gallery') {
      var mainFolder = DriveApp.getFolderById(GALLERY_FOLDER_ID);
      var subfolders = mainFolder.getFolders();
      var projects = [];
      while (subfolders.hasNext()) {
        var subfolder = subfolders.next();
        var files2 = subfolder.getFiles();
        var photos2 = [];
        while (files2.hasNext()) {
          var img = files2.next();
          if (img.getMimeType().indexOf('image') === -1) continue;
          photos2.push({name: img.getName(), url: 'https://drive.google.com/uc?export=view&id=' + img.getId()});
        }
        photos2.sort(function(a,b){return a.name.localeCompare(b.name);});
        if (photos2.length) projects.push({project: subfolder.getName(), photos: photos2});
      }
      projects.sort(function(a,b){return a.project.localeCompare(b.project);});
      return ContentService.createTextOutput(JSON.stringify(projects)).setMimeType(ContentService.MimeType.JSON);
    }
    return ContentService.createTextOutput('SL Installations API').setMimeType(ContentService.MimeType.TEXT);
  } catch(err) {
    return ContentService.createTextOutput(JSON.stringify({error:err.toString()})).setMimeType(ContentService.MimeType.JSON);
  }
}

function shareAllFiles() {
  var mainFolder = DriveApp.getFolderById(GALLERY_FOLDER_ID);
  var subfolders = mainFolder.getFolders();
  while (subfolders.hasNext()) {
    var sub = subfolders.next();
    sub.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    var files = sub.getFiles();
    while (files.hasNext()) { files.next().setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW); }
  }
  var featured = DriveApp.getFolderById(FEATURED_FOLDER_ID);
  featured.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
  var fFiles = featured.getFiles();
  while (fFiles.hasNext()) { fFiles.next().setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW); }
  Logger.log('Done - all files shared');
}
