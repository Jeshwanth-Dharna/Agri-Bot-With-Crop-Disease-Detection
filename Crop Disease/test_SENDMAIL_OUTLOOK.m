function test_SENDMAIL_OUTLOOK()
recipients = 'jeshwanthdharna23@gmail.com';
emailSubject = 'Test subject';
textBody = 'Test message including an image';
imageBody1 = '';
imageBody2 = '';
mainBody = [textBody '<p>' imageBody1 '<p>' imageBody2];
attachement1 = 'D:\new\final.m';
attachement2 = 'D:\new\mainn.m';
attachements = {attachement1 attachement2};
sendolmail(recipients,emailSubject, mainBody, attachements);
end
function sendolmail(to,subject,body,attachments)
%Sends email using MS Outlook. The format of the function is
%Similar to the SENDMAIL command.
% Create object and set parameters.
h = actxserver('outlook.Application');
mail = h.CreateItem('olMail');
mail.Subject = subject;
mail.To = to;
mail.BodyFormat = 'olFormatHTML';
mail.HTMLBody = body;
% Add attachments, if specified.
if nargin == 4
    for i = 1:length(attachments)
        mail.attachments.Add(attachments{i});
    end
end
% Send message and release object.
mail.Send;
h.release;
end