////////////////////////////////////////////////////////////////////////////////
// ----------------------------------------------------------------------------
// ..\Tests\ETRSysAdmin.tst
//
// Script for Partner TUI System Administration for TUI
//
// Duration to run on target: 20min
//
// Modification History
// YYMMDD Name                    Comment
// 110124 Mihai Manolache         Initial Creation
//
// ----------------------------------------------------------------------------
////////////////////////////////////////////////////////////////////////////////
main:
{
    // Enable debug output from script parser
    set:Scripter.debug = True;

    set:Variable.delay_time = 2000;

    set:Variable.sync_delay_time = 6000;

    set:Variable.wait_time =1500;

    set:Variable.idle_time = 3000;

    report(**** System Administration Tests ****):<null>;

    // Test System Administration  menu items
    set:Variable.numTests=7;
    set:Variable.testNumber=1;
    while($testNumber <= $numTests):
    {
        gosub:TestCase$testNumber;
        set:Variable.testNumber = $testNumber+1;
    }

    // Make sure the phone is put onhook at the end of the tests
    set:User(Extn11).cm_extn.DCP.HookChange = OnHook;
    wait:$idle_time;

}

TestCase1:
{
    report(********** TestCase1 STARTED  ************):<null>;
    report(********** System Data **********):<null>;
    gosub:SetGlobals_Extn11;
    gosub:Configuration;
    gosub:TestMenuItem_SystemDate;
    gosub:Deconfiguration;
    report(********** TestCase1 COMPLETED ************):<null>;
}

TestCase2:
{
    report(********** TestCase2 STARTED  ************):<null>;
    report(********** System Time **********):<null>;
    gosub:SetGlobals_Extn11;
    gosub:Configuration;
    gosub:TestMenuItem_SystemTime;
    gosub:Deconfiguration;
    report(********** TestCase2 COMPLETED ************):<null>;
}

TestCase3:
{
    report(********** TestCase3 STARTED  ************):<null>;
    report(********** Number of lines **********):<null>;
    gosub:SetGlobals_Extn11;
    gosub:Configuration;
    gosub:TestMenuItem_NumberOfLines;
    gosub:Deconfiguration;
    report(********** TestCase3 COMPLETED ************):<null>;
}

TestCase4:
{
    report(********** TestCase4 STARTED ************):<null>;
    report(********** Transfer Return **********):<null>;
    gosub:SetGlobals_Extn11;
    gosub:Configuration;
    gosub:TestMenuItem_TransferReturn;
    gosub:Deconfiguration;
    report(********** TestCase4 COMPLETED ************):<null>;
}

TestCase5:
{
    report(********** TestCase5 STARTED ************):<null>;
    report(********** RecallTimerDuration **********):<null>;
    gosub:SetGlobals_Extn11;
    gosub:Configuration;
    gosub:TestMenuItem_RecallTimerDuration;
    gosub:Deconfiguration;
    report(********** TestCase5 COMPLETED ************):<null>;
}

TestCase6:
{
    report(********** TestCase6 STARTED ************):<null>;
    report(********** OutsideConferenceDenial **********):<null>;
    gosub:SetGlobals_Extn11;
    gosub:Configuration;
    gosub:TestMenuItem_OutsideConfDenial;
    gosub:Deconfiguration;
    report(********** TestCase6 COMPLETED ************):<null>;
}

TestCase7:
{
    report(********** TestCase7 STARTED ************):<null>;
    report(********** RingingOnTransfer **********):<null>;
    gosub:SetGlobals_Extn11;
    gosub:Configuration;
    gosub:TestMenuItem_RingingOnTransfer;
    gosub:Deconfiguration;
    report(********** TestCase7 COMPLETED ************):<null>;
}

///////////////////////////////////////////////////////////////////////////////
//                              TESTS                                        //
///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
TestMenuItem_SystemDate:
{

    set:Partner($UserName).OffHook;
    set:User($UserName).cm_extn.DCP.HookChange = OnHook;
    set:User($UserName).cm_extn.DCP.HookChange = OnHook;
    wait:$idle_time;

    gosub:IdleAdminX;
    wait:$wait_time;

    gosub:IdleToSystemAdmin;

    set:User($UserName).cm_extn.DCP.StdKey =#;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#1                      ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =0;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#10                     ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="System Date:            ";
    set:Variable.line2="";// we don't want to check this line
    gosub:TestDisplayedLines;
    wait:$wait_time;
}

TestMenuItem_SystemTime:
{
    set:User($UserName).cm_extn.DCP.StdKey =#;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#1                      ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =0;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#10                     ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =3;
    wait:$wait_time;
    set:Variable.line1="System Time:            ";
    set:Variable.line2="";// we don't want to check this line //HHMM: xxxx
    gosub:TestDisplayedLines;
    wait:$wait_time;
}

TestMenuItem_NumberOfLines:
{
    gosub:IdleToSystemAdmin;
    set:User($UserName).cm_extn.DCP.StdKey =#;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#1                      ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =0;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#10                     ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =4;
    wait:$wait_time;
    set:Variable.line1="Number of Lines:";
    set:Variable.line2="";
    gosub:TestDisplayedLines;
    wait:$wait_time;
    wait:$wait_time;

    //Enter 00 lines
    set:User($UserName).cm_extn.DCP.StdKey =0;
    wait:$wait_time;
    set:Variable.line1="Number of Lines:";
    set:Variable.line2="0";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =0;
    wait:$wait_time;

    set:Variable.line1="Number of Lines:        ";
    set:Variable.line2="00 Lines                ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //Press digit 6
    set:User($UserName).cm_extn.DCP.StdKey =6;
    wait:$wait_time;
    set:Variable.line1="Number of Lines:        ";
    set:Variable.line2="6                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //Press digit 5-> form 65 (invalid data - screen should remain unchanged)
    set:User($UserName).cm_extn.DCP.StdKey =5;
    wait:$wait_time;
    set:Variable.line1="Number of Lines:        ";
    set:Variable.line2="6                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //Press digit 4-> form 64
    set:User($UserName).cm_extn.DCP.StdKey =4;
    wait:$wait_time;
    set:Variable.line1="Number of Lines:        ";
    set:Variable.line2="64 Lines                ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //test circular values
    gosub:PressNextData;
    wait:$wait_time;

    set:Variable.line1="Number of Lines:        ";
    set:Variable.line2="00 Lines                ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    gosub:PressDefault;

    set:Variable.line1="Number of Lines:        ";
    set:Variable.line2="";// don't check this.
    gosub:TestDisplayedLines;
    wait:$wait_time;
}


TestMenuItem_TransferReturn:
{
    gosub:IdleToSystemAdmin;
    set:User($UserName).cm_extn.DCP.StdKey =#;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#1                      ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =0;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#10                     ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =5;
    wait:$wait_time;
    set:Variable.line1="Transfer Return:        ";
    set:Variable.line2="";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =0;
    wait:$wait_time;
    set:Variable.line1="Transfer Return:        ";
    set:Variable.line2="0 No Transfer Return    ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="Transfer Return:        ";
    set:Variable.line2="1 Rings                 ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =2;
    wait:$wait_time;
    set:Variable.line1="Transfer Return:        ";
    set:Variable.line2="2 Rings                 ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =3;
    wait:$wait_time;
    set:Variable.line1="Transfer Return:        ";
    set:Variable.line2="3 Rings                 ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =4;
    wait:$wait_time;
    set:Variable.line1="Transfer Return:        ";
    set:Variable.line2="4 Rings                 ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =5;
    wait:$wait_time;
    set:Variable.line1="Transfer Return:        ";
    set:Variable.line2="5 Rings                 ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =6;
    wait:$wait_time;
    set:Variable.line1="Transfer Return:        ";
    set:Variable.line2="6 Rings                 ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:$wait_time;
    set:Variable.line1="Transfer Return:        ";
    set:Variable.line2="7 Rings                 ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =8;
    wait:$wait_time;
    set:Variable.line1="Transfer Return:        ";
    set:Variable.line2="8 Rings                 ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =9;
    wait:$wait_time;
    set:Variable.line1="Transfer Return:        ";
    set:Variable.line2="9 Rings                 ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    gosub:PressNextData;
    wait:$wait_time;
    set:Variable.line1="Transfer Return:        ";
    set:Variable.line2="0 No Transfer Return    ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    gosub:PressPrevData;
    wait:$wait_time;
    set:Variable.line1="Transfer Return:        ";
    set:Variable.line2="9 Rings                 ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    gosub:PressDefault;
    wait:$wait_time;
    set:Variable.line1="Transfer Return:        ";
    set:Variable.line2="4 Rings                 ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

}


TestMenuItem_RecallTimerDuration:
{
    gosub:IdleToSystemAdmin;
    set:User($UserName).cm_extn.DCP.StdKey =#;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =1;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#1                      ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =0;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#10                     ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:$wait_time;
    set:Variable.line1="Recall Timer Duration:  ";
    set:Variable.line2="";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    // valid values are from 01 to 80. Try an invalid value 00
    set:User($UserName).cm_extn.DCP.StdKey =0;
    wait:$wait_time;
    set:Variable.line1="Recall Timer Duration:  ";
    set:Variable.line2="0                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =0;
    wait:$wait_time;
    set:Variable.line1="Recall Timer Duration:  ";
    set:Variable.line2="0                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //press digit 1 -> 01
    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="Recall Timer Duration:  ";
    set:Variable.line2="01   25-msec            ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //press NextData
    gosub:PressNextData;
    wait:$wait_time;
    set:Variable.line1="Recall Timer Duration:  ";
    set:Variable.line2="02   50-msec            ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //insert an invalid value. e.g 81
    set:User($UserName).cm_extn.DCP.StdKey =8;
    wait:$wait_time;
    set:Variable.line1="Recall Timer Duration:  ";
    set:Variable.line2="8                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="Recall Timer Duration:  ";
    set:Variable.line2="8                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //press digit 0 ->80
    set:User($UserName).cm_extn.DCP.StdKey =0;
    wait:$wait_time;
    set:Variable.line1="Recall Timer Duration:  ";
    set:Variable.line2="80 2000-msec            ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //press DEFAULT
    gosub:PressDefault;
    wait:$wait_time;
    set:Variable.line1="Recall Timer Duration:  ";
    set:Variable.line2="20  500-msec            ";
    gosub:TestDisplayedLines;
    wait:$wait_time;
}

TestMenuItem_OutsideConfDenial:
{
    gosub:IdleToSystemAdmin;
    set:User($UserName).cm_extn.DCP.StdKey =#;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#1                      ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =0;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#10                     ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =9;
    wait:$wait_time;
    set:Variable.line1="Outside Conf Denial:    ";
    set:Variable.line2="";
    gosub:TestDisplayedLines;
    wait:$wait_time;

      //press 2 - Disallowed
    set:User($UserName).cm_extn.DCP.StdKey =2;
    wait:$wait_time;
    set:Variable.line1="Outside Conf Denial:    ";
    set:Variable.line2="2 Disallowed            ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //press 1 - Allowed
    set:User($UserName).cm_extn.DCP.StdKey =2;
    wait:$wait_time;
    set:Variable.line1="Outside Conf Denial:    ";
    set:Variable.line2="2 Disallowed            ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //press an invalid digit
    set:User($UserName).cm_extn.DCP.StdKey =3;
    wait:$wait_time;
    set:Variable.line1="Outside Conf Denial:    ";
    set:Variable.line2="2 Disallowed            ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //Default
    gosub:PressDefault;
    wait:$wait_time;
    set:Variable.line1="Outside Conf Denial:    ";
    set:Variable.line2="1 Allowed               ";
    gosub:TestDisplayedLines;
    wait:$wait_time;
}

TestMenuItem_WakeUpServiceButton:
{
    gosub:IdleToSystemAdmin;
    set:User($UserName).cm_extn.DCP.StdKey =#;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#1                      ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#11                     ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =5;
    wait:$wait_time;
    //check default 2 - Not Assigned
    set:Variable.line1="Wake Up Service Button: ";
    set:Variable.line2="2 Not Assigned          ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //press digit 1
    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="Wake Up Service Button: ";
    set:Variable.line2="1 Assigned - Ext 10     ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //press an invalid digit
    set:User($UserName).cm_extn.DCP.StdKey =4;
    wait:$wait_time;
    set:Variable.line1="Wake Up Service Button: ";
    set:Variable.line2="1 Assigned - Ext 10     ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

      //press 3 to chose button
      set:User($UserName).cm_extn.DCP.StdKey =3;
    wait:$wait_time;
    set:Variable.line1="Wake Up Service Button: ";
    set:Variable.line2="Button:                 ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

      //press digits 1 1 for button11
      set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="Wake Up Service Button: ";
    set:Variable.line2="1                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

      set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
      verify(GreenLamp 11 of USER=$UserName is Off):User($UserName).cm_extn.DCP.DSS[10].GreenLamp=On;
    verify(GreenLamp 11 of USER=$UserName is Off):User($UserName).cm_extn.DCP.DSS[10].RedLamp=Off;
      set:Variable.line1="Wake Up Service Button: ";
    set:Variable.line2="1 Assigned - Ext 10     ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    //Default
    gosub:PressDefault;
    wait:$wait_time;
    set:Variable.line1="Wake Up Service Button: ";
    set:Variable.line2="2 Not Assigned          ";
    gosub:TestDisplayedLines;
    wait:$wait_time;
}

TestMenuItem_RingingOnTransfer:
{
    gosub:IdleToSystemAdmin;
    set:User($UserName).cm_extn.DCP.StdKey =#;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#                       ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#1                      ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="System Administration:  ";
    set:Variable.line2="#11                     ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =9;
    wait:$wait_time;
    set:Variable.line1="Ringing on Transfer:    ";
    set:Variable.line2="";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =1;
    wait:$wait_time;
    set:Variable.line1="Ringing on Transfer:    ";
    set:Variable.line2="1 Active                ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =2;
    wait:$wait_time;
    set:Variable.line1="Ringing on Transfer:    ";
    set:Variable.line2="2 Not Active            ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    set:User($UserName).cm_extn.DCP.StdKey =3;
    wait:$wait_time;
    set:Variable.line1="Ringing on Transfer:    ";
    set:Variable.line2="2 Not Active            ";
    set:Variable.line3="                        ";
    set:Variable.line4="        Default   Back  ";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    gosub:PressDefault;
    wait:$wait_time;
    set:Variable.line1="Ringing on Transfer:    ";
    set:Variable.line2="1 Active                ";
    set:Variable.line3="                        ";
    set:Variable.line4="        Default   Back  ";
    gosub:TestDisplayedLines;
    wait:$wait_time;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////


SetGlobals_Extn10:
{
    set:Variable.line1="                        ";
    set:Variable.line2="                        ";
    set:Variable.UserName =$x10_UserName;
    set:Variable.IsETR   =$x10_IsETR;
    set:Variable.NumLines =$x10_NumLines;
    set:Variable.PhoneType =$x10_PhoneType;
    set:Variable.Type = $x10_Type;
    set:Variable.SystemPhone=True;
    set:Variable.UserNum=10;
}

SetGlobals_Extn11:
{
    set:Variable.line1="                        ";
    set:Variable.line2="                        ";
    set:Variable.line3="                        ";
    set:Variable.line4="";
    set:Variable.UserName =$x11_UserName;
    set:Variable.IsSage   =$x11_IsSage;
    set:Variable.NumLines =$x11_NumLines;
    set:Variable.PhoneType =$x11_PhoneType;
    set:Variable.Type = $x11_Type;
    set:Variable.SystemPhone=True;
    set:Variable.UserNum=11;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

TestDisplayedLines:
{
    report(Test $NumLines lines for $UserName ):<null>;
    if($line1!=''): //hack
    {
        report(line1=$line1):<null>;
    }
    if($line2!=''): //hack
    {
        report(line2=$line2):<null>;
    }

    if($line1!=''):
    {
        verify(1st line of menu display incorrect):User($UserName).cm_extn.DCP.Display[0]=$line1;
    }
    if($line2!=''):
    {
        verify(2nd line of menu display incorrect):User($UserName).cm_extn.DCP.Display[1]=$line2;
    }
}

IdleToSystemAdmin:
{
    report( SYSTEM ADMINISTRATION ):<null>;
}

IdleAdminX:
{
      gosub:PressFeature00;
    wait:$wait_time;

    set:Variable.line1="Program Extension";
    set:Variable.line2="";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    gosub:PressIcom1;
    wait:$wait_time;

    set:Variable.line1="Extension Name";
    set:Variable.line2="";
    gosub:TestDisplayedLines;
    wait:$wait_time;

    gosub:PressIcom1;
    wait:$wait_time;

    set:Variable.line1="System Administration";
    set:Variable.line2="";
    gosub:TestDisplayedLines;
    wait:$wait_time;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

Configuration:
{
    report(*** ETR configuration ***):<null>;

    //set:Partner($UserName).OffHook;
    //set:User($UserName).cm_extn.DCP.HookChange = OnHook;
    wait:$idle_time;

}

Deconfiguration:
{
    report(*** ETR deconfiguration ***):<null>;

    //set:Partner($UserName).OffHook;
    //set:User($UserName).cm_extn.DCP.HookChange = OnHook;
    wait:$idle_time;
}

PressExit:
{
    report(PressExit):<null>;
    set:User($UserName).cm_extn.DCP.MenuKey = Exit;
}

PressNextData:
{
    report(Press Next_Data):<null>;
    //press next_data
    if($Type==ETR18D):
    {
        set:User($UserName).cm_extn.DCP.DSS[16]=Press;
    }
    else if($Type==ETR34D):
    {
        set:User($UserName).cm_extn.DCP.DSS[29]=Press;
    }
}

PressPrevData:
{
    report(Press Prev_Data):<null>;
        //press prev_data
    if($Type==ETR18D):
    {
        set:User($UserName).cm_extn.DCP.DSS[12]=Press;
    }
    if($Type==ETR34D):
    {
        set:User($UserName).cm_extn.DCP.DSS[23]=Press;
    }
}

PressNextItem:
{
    report(Press Next_Item):<null>;
        //press next_item
    if($Type==ETR18D):
    {
        set:User($UserName).cm_extn.DCP.DSS[15]=Press;
    }
    else if($Type==ETR34D):
    {
        set:User($UserName).cm_extn.DCP.DSS[28]=Press;
    }
}

PressPrevItem:
{
    report(Press Prev_Item):<null>;
    //press prev_item
    if($Type==ETR18D):
    {
        set:User($UserName).cm_extn.DCP.DSS[11]=Press;
    }
    else if($Type==ETR34D):
    {
        set:User($UserName).cm_extn.DCP.DSS[22]=Press;
    }
}

PressNextProcedure:
{
    report(Press Next_Procedure ):<null>;
        //press next_procedure
    if($Type==ETR18D):
    {
        set:User($UserName).cm_extn.DCP.DSS[14]=Press;
    }
    else if($Type==ETR34D):
    {
        set:User($UserName).cm_extn.DCP.DSS[27]=Press;
    }
}

PressPrevProcedure:
{
    report(Press Prev_Procedure):<null>;

    //press prev_procedure
    if($Type==ETR18D):
    {
        set:User($UserName).cm_extn.DCP.DSS[10]=Press;
    }
    else if($Type==ETR34D):
    {
        set:User($UserName).cm_extn.DCP.DSS[21]=Press;
    }
}

PressDefault:
{
    if($Type==ETR18D):
    {
        set:User($UserName).cm_extn.DCP.DSS[17]=Press;
    }
    else if($Type==ETR34D):
    {
        set:User($UserName).cm_extn.DCP.DSS[30]=Press;
    }
}

PressEnter:
{
    if($Type==ETR18D):
    {
        set:User($UserName).cm_extn.DCP.DSS[13]=Press;
    }
    else if($Type==ETR34D):
    {
        set:User($UserName).cm_extn.DCP.DSS[24]=Press;
    }
}

PressFeature00:
{
    set:User($UserName).cm_extn.DCP.FeatureKey =DCPLFeatureFeature;

    set:User($UserName).cm_extn.DCP.StdKey =0;

    set:User($UserName).cm_extn.DCP.StdKey =0;

}

PressIcom1:
{
    set:User($UserName).cm_extn.DCP.DSS[0] =Press;
}

PressIcom2:
{
    set:User($UserName).cm_extn.DCP.DSS[1] =Press;
}

Insert_a:
{
    set:User($UserName).cm_extn.DCP.StdKey =2;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =2;
    wait:100;
    wait:1000;
}

Insert_b:
{
    set:User($UserName).cm_extn.DCP.StdKey =2;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =2;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =2;
    wait:100;
    wait:1000;
}

Insert_c:
{
    set:User($UserName).cm_extn.DCP.StdKey =2;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =2;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =2;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =2;
    wait:100;
    wait:1000;
}

Insert_d:
{
    set:User($UserName).cm_extn.DCP.StdKey =3;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =3;
    wait:100;
    wait:1000;
}

Insert_e:
{
    set:User($UserName).cm_extn.DCP.StdKey =3;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =3;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =3;
    wait:100;
    wait:1000;
}

Insert_f:
{
    set:User($UserName).cm_extn.DCP.StdKey =3;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =3;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =3;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =3;
    wait:100;
    wait:1000;
}

Insert_g:
{
    set:User($UserName).cm_extn.DCP.StdKey =4;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =4;
    wait:100;
    wait:1000;
}

Insert_h:
{
    set:User($UserName).cm_extn.DCP.StdKey =4;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =4;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =4;
    wait:100;
    wait:1000;
}

Insert_i:
{
    set:User($UserName).cm_extn.DCP.StdKey =4;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =4;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =4;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =4;
    wait:100;
    wait:1000;
}

Insert_j:
{
    set:User($UserName).cm_extn.DCP.StdKey =5;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =5;
    wait:100;
    wait:1000;
}

Insert_k:
{
    set:User($UserName).cm_extn.DCP.StdKey =5;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =5;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =5;
    wait:100;
    wait:1000;
}

Insert_l:
{
    set:User($UserName).cm_extn.DCP.StdKey =5;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =5;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =5;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =5;
    wait:100;
    wait:1000;
}

Insert_m:
{
    set:User($UserName).cm_extn.DCP.StdKey =6;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =6;
    wait:100;
    wait:1000;
}

Insert_n:
{
    set:User($UserName).cm_extn.DCP.StdKey =6;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =6;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =6;
    wait:100;
    wait:1000;
}

Insert_o:
{
    set:User($UserName).cm_extn.DCP.StdKey =6;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =6;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =6;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =6;
    wait:100;
    wait:1000;
}

Insert_m:
{
    set:User($UserName).cm_extn.DCP.StdKey =6;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =6;
    wait:100;
    wait:1000;
}

Insert_p:
{
    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:100;
    wait:1000;
}

Insert_q:
{
    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:100;
    wait:1000;
}

Insert_r:
{
    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:100;
    wait:1000;
}

Insert_s:
{
    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =7;
    wait:100;
    wait:1000;
}

Insert_t:
{
    set:User($UserName).cm_extn.DCP.StdKey =8;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =8;
    wait:100;
    wait:1000;
}

Insert_u:
{
    set:User($UserName).cm_extn.DCP.StdKey =8;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =8;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =8;
    wait:100;
    wait:1000;
}

Insert_v:
{
    set:User($UserName).cm_extn.DCP.StdKey =8;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =8;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =8;
    wait:100;
    set:User($UserName).cm_extn.DCP.StdKey =8;
    wait:100;
    wait:1000;
}

EnterTelephoneProgramming:
{
    if( $IsSage ==True ):
    {
        if( $SystemPhone ==True):
        {
            gosub:PressSoftKey3;
            wait:$wait_time;

            gosub:PressDownArrow;
            wait:$wait_time;

            gosub:PressDownArrow;
            wait:$wait_time;

            gosub:PressSoftKey1;   // Select Telephone Programming
            wait:$wait_time;
        }
        if( $SystemPhone ==False):
        {
            gosub:PressSoftKey3;
            wait:$wait_time;

            gosub:PressSoftKey1;   // Select Telephone Programming
            wait:$wait_time;
        }
    }
    if($IsSage ==False):
    {
        //report(*****TO BE IMPLEMENTED):<null>;
        gosub:PressFeature00;
        wait:$wait_time;
    }
}

EnterButtonProgramming:
{
    gosub:EnterTelephoneProgramming;

    if($IsSage ==True):
    {
        gosub:PressDownArrow;//line ringing
        wait:$wait_time;

        gosub:PressDownArrow;//personal speed dial
        wait:$wait_time;

        gosub:PressDownArrow;//system speed dial
        wait:$wait_time;

        gosub:PressDownArrow;//button programming
        wait:$wait_time;

        gosub:PressEnter;
        wait:$wait_time;
    }
    if($IsSage ==False):
    {
        report(***** Enter Button Programming sage=$IsSage):<null>;
    }
}



PressDSSKey:
{
    report(***PressDSSKey  $dssKey):<null>;
    set:Variable.mappedType = False;
    if($PhoneType ==1508):
    {
        set:Variable.mappedType = True;
        if($dssKey==0):
        {
            set:User($UserName).cm_extn.DCP.DSS[4]=Press;
        }
        if($dssKey==1):
        {
            set:User($UserName).cm_extn.DCP.DSS[5]=Press;
        }
        if($dssKey==2):
        {
            set:User($UserName).cm_extn.DCP.DSS[6]=Press;
        }
        if($dssKey==3):
        {
            set:User($UserName).cm_extn.DCP.DSS[7]=Press;
        }
        if($dssKey==4):
        {
            set:User($UserName).cm_extn.DCP.DSS[0]=Press;
        }
        if($dssKey==5):
        {
            set:User($UserName).cm_extn.DCP.DSS[1]=Press;
        }
        if($dssKey==6):
        {
            set:User($UserName).cm_extn.DCP.DSS[2]=Press;
        }
        if($dssKey==7):
        {
            set:User($UserName).cm_extn.DCP.DSS[3]=Press;
        }
    }
    if($PhoneType ==1516):
    {
        set:Variable.mappedType = True;
        if($dssKey==0):
        {
            set:User($UserName).cm_extn.DCP.DSS[15]=Press;
        }
        if($dssKey==1):
        {
            set:User($UserName).cm_extn.DCP.DSS[14]=Press;
        }
        if($dssKey==2):
        {
            set:User($UserName).cm_extn.DCP.DSS[13]=Press;
        }
        if($dssKey==3):
        {
            set:User($UserName).cm_extn.DCP.DSS[12]=Press;
        }
        if($dssKey==4):
        {
            set:User($UserName).cm_extn.DCP.DSS[11]=Press;
        }
        if($dssKey==5):
        {
            set:User($UserName).cm_extn.DCP.DSS[10]=Press;
        }
        if($dssKey==6):
        {
            set:User($UserName).cm_extn.DCP.DSS[9]=Press;
        }
        if($dssKey==7):
        {
            set:User($UserName).cm_extn.DCP.DSS[8]=Press;
        }
        if($dssKey==8):
        {
            set:User($UserName).cm_extn.DCP.DSS[7]=Press;
        }
        if($dssKey==9):
        {
            set:User($UserName).cm_extn.DCP.DSS[6]=Press;
        }
        if($dssKey==10):
        {
            set:User($UserName).cm_extn.DCP.DSS[5]=Press;
        }
        if($dssKey==11):
        {
            set:User($UserName).cm_extn.DCP.DSS[4]=Press;
        }
        if($dssKey==12):
        {
            set:User($UserName).cm_extn.DCP.DSS[3]=Press;
        }
        if($dssKey==13):
        {
            set:User($UserName).cm_extn.DCP.DSS[2]=Press;
        }
        if($dssKey==14):
        {
            set:User($UserName).cm_extn.DCP.DSS[1]=Press;
        }
        if($dssKey==15):
        {
            set:User($UserName).cm_extn.DCP.DSS[0]=Press;
        }
    }

    if($mappedType ==False ):
    {
        set:User($UserName).cm_extn.DCP.DSS[$dssKey]=Press;
    }
    report(***PressDSSKey END ):<null>;
}


ExitFeature:
{
    report(****ExitFeature):<null>;
    if($IsSage ==True):
    {
        gosub:PressExit;
        wait:$wait_time;
    }

    if($IsSage ==False):
    {
        gosub:PressFeature00;
        wait:$wait_time;
    }
}

ClearFeature:
{
    report(***ClearFeature***):<null>;
    if($IsSage ==True):
    {
        gosub:PressSoftKey2; //clear feature
        wait:$wait_time;
    }

    if($IsSage ==False):
    {
        set:User($UserName).cm_extn.DCP.FeatureKey=DCPLFeatureMIC;
        wait:$wait_time;
    }
}

// it will be followed by some digits
ProgramFeature:
{
    report(*** Program Feature):<null>;
    if($IsSage ==True):
    {
        gosub:PressSoftKey1; //Program
        wait:$wait_time;

        // #
        set:User($UserName).cm_extn.DCP.StdKey =#;
        wait:100;
    }
    if($IsSage ==False):
    {
        set:User($UserName).cm_extn.DCP.FeatureKey =DCPLFeatureFeature;
        wait:$wait_time;
    }
}
