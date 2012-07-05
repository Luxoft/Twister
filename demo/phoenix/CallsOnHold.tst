////////////////////////////////////////////////////////////////////////////////
// ----------------------------------------------------------------------------
// ..\Tests\Partner\CallProcessing\CallsOnHold.tst
//
// Script for Partner ETR, 14xx, 95xx and Nortel phones
//
// Duration to run on target: ??min
//
// Modification History
// YYMMDD Name                    Comment
// 120406 Adrian Simionescu       Initial Creation
//
// ----------------------------------------------------------------------------
////////////////////////////////////////////////////////////////////////////////
main:
{
    ////////////////////////////////////////////
    // Enable debug output from script parser //
    ////////////////////////////////////////////
    set:Scripter.debug = True;

    //////////////////////
    // Default timmings //
    //////////////////////
    set:Variable.delay_time = 2000;
    set:Variable.sync_delay_time_time = 6000;
    set:Variable.wait_time = 1000;
    set:Variable.connect_time=10000;
    set:Variable.ring_time=15000;
    set:Variable.ring_time_POTS=15000;
    set:Variable.transfer_ring_time=5000;
    set:Variable.idle_time=5000;
    set:Variable.VM_connect_time=20000;
    set:Variable.hold_time=5000;
    set:Variable.test_delay=10000;
    set:Variable.PRILineSubtype=PRI;
    set:Variable.answertime= 3000;
    set:Variable.lamptime = 3000;
    set:Variable.screen_sync_delay_time_time = 5000;

    report(**** Calls on Hold Tests STARTED ****):<null>;
    if($RunMode == Rig):
    {
        wait:180000;
    }
    // For Simulator, 5 seconds should enough for the VM to start up
    if($RunMode == Simulator):
    {
        wait:5000;
    }

    //////////////////////////
    // Run Acceptance Tests //
    //////////////////////////
    set:Variable.TestID=1;  //1
    set:Variable.TestEnd=4;
    while($TestID <= $TestEnd):
    {
        gosub:TestCase$TestID;
        set:Variable.TestID = $TestID + 1;
        wait:$wait_time;
    }
    // Line Appearances are missing on Extn19 and Extn20 after the tests finish
    // We need to clean the config
    report(**** Calls on Hold Tests COMPLETED ****):<null>;
}

///////////////////////////////////////////////////////////////////////////////////////
////////////////////////         CALLS ON HOLD TESTS         //////////////////////////
///////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////////
// Test1                                                                       //
//    SCENARIO (1): ETR Phone Display – Internal&External Calls                //
/////////////////////////////////////////////////////////////////////////////////
TestCase1:
{
    report(********** Calls on Hold Test 1 - TestCase1 STARTED **********):<null>;
    set:Variable.CallExtern = 0;
    gosub:Configuration;
    gosub:TestInternalCallsOnHold;
    gosub:Deconfiguration;

    set:Variable.CallExtern = 1;
    gosub:Configuration;
    gosub:TestExternalCallsOnHold;
    gosub:Deconfiguration;
    report(********** Calls on Hold Test 1 - TestCase1 COMPLETED **********):<null>;
}

/////////////////////////////////////////////////////////////////////////////////
//  Test2                                                                      //
//    SCENARIO (1): 1400 Phone Display – Internal&External Calls               //
/////////////////////////////////////////////////////////////////////////////////
TestCase2:
{
    report(********** Calls on Hold Test 2 - TestCase2 STARTED **********):<null>;
    set:Variable.CallExtern = 0;
    gosub:Configuration;
    gosub:TestInternalCallsOnHold;
    gosub:Deconfiguration;

    set:Variable.CallExtern = 1;
    gosub:Configuration;
    gosub:TestExternalCallsOnHold;
    gosub:Deconfiguration;
    report(********** Calls on Hold Test 2 - TestCase2 COMPLETED **********):<null>;
}
/////////////////////////////////////////////////////////////////////////////////
//  Test3                                                                      //
//    SCENARIO (1): 9500 Phone Display – Internal&External Calls               //
/////////////////////////////////////////////////////////////////////////////////
TestCase3:
{
    report(********** Calls on Hold Test 3 -9500 Phones- TestCase3 STARTED **********):<null>;
    set:Variable.CallExtern = 0;
    gosub:Configuration;
    gosub:TestInternalCallsOnHold;
    gosub:Deconfiguration;

    set:Variable.CallExtern = 1;
    gosub:Configuration;
    gosub:TestExternalCallsOnHold;
    gosub:Deconfiguration;
    report(********** Calls on Hold Test 3 -9500 Phones- TestCase3 COMPLETED **********):<null>;
}
/////////////////////////////////////////////////////////////////////////////////
//  Test4                                                                      //
//    SCENARIO (1): 9500 Phone Display – Internal&External Calls               //
/////////////////////////////////////////////////////////////////////////////////
TestCase4:
{
    report(********** Calls on Hold Test 4 -9500 Phones- TestCase4 STARTED **********):<null>;
    set:Variable.CallExtern = 0;
    gosub:Configuration;
    gosub:TestInternalCallsOnHold;
    gosub:Deconfiguration;

    set:Variable.CallExtern = 1;
    gosub:Configuration;
    gosub:TestExternalCallsOnHold;
    gosub:Deconfiguration;
    report(********** Calls on Hold Test 4 -9500 Phones- TestCase4 COMPLETED **********):<null>;
}

////////////////////////////////////////////////////////////////////////////////

////////////////////
//  CALL SCRIPTS  //
////////////////////

/////////////////////////////////////////////////
// Calls on Hold - Internal Calls              //
/////////////////////////////////////////////////
TestInternalCallsOnHold:
{
    report:(***** START Test Internal Calls on Hold ******):<null>;

    wait:$delay_time;

    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = $TypeA;set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = $TypeB;set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $BIncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A offhook
    set:User($UserA).cm_extn.DCP.DSS[$AOutgoingCall_dssKey] = Press;
    //wait:$delay_time;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // User A DIAL
    set:Variable.Usr = $UserA;set:Variable.State = "DIAL";set:Variable.PType = $TypeA;set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // A dials B
    set:User($UserA).cm_extn.DialWithGaps.1000=$ExtnB;
    wait:$ring_time;

    // User B RINGING and User A RINGBACK
    sync($sync_delay_time_time):User($UserB).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time_time):User($UserA).cm_extn.current_ep.state=CMCSRingBack;

    // User A RINGBACK
    set:Variable.Usr = $UserA;set:Variable.State = "RINGBACK";set:Variable.PType = $TypeA;set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B RING
    set:Variable.Usr = $UserB;set:Variable.State = "RING";set:Variable.PType = $TypeB;set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $BIncomingCall_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B Answers
    set:User($UserB).cm_extn.DCP.DSS[$BIncomingCall_dssKey] = Press;
    wait:$hold_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A CONN
    set:Variable.Usr = $UserA;set:Variable.State = "CONN";set:Variable.PType = $TypeA;set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B CONN
    set:Variable.Usr = $UserB;set:Variable.State = "CONN";set:Variable.PType = $TypeB;set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $BIncomingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    set:Variable.Usr = $UserA;set:Variable.PType = $TypeA;
    gosub:PressHOLDKey;  // push Hold button
    wait:$wait_time;

    verify:User($UserA).cm_extn.state = CMESIdle;
    verify:User($UserB).cm_extn.state = CMESConnected;

    set:Variable.Usr = $UserA;set:Variable.State = "HOLD";set:Variable.PType = $TypeA;set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="Flush";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    set:Variable.Usr = $UserB;set:Variable.State = "HELD";set:Variable.PType = $TypeB;set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $BIncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Wink";
    if( $PType == "ETR" ):
    {
        set:Variable.GreenLp ="On";
        set:Variable.RedLp ="Off";
    }
    gosub:CheckLamps;

    wait:$connect_time;
    wait:$connect_time;
    wait:$connect_time;

    // User A RINGING and User A CONNECTED
    sync($sync_delay_time_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    set:Variable.Usr = $UserA;set:Variable.State = "BACKCALL";set:Variable.PType = $TypeA;set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="Flush";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    set:Variable.Usr = $UserB;set:Variable.State = "HELD";set:Variable.PType = $TypeB;set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $BIncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Wink";
    if( $PType == "ETR" ):
    {
        set:Variable.GreenLp ="On";
        set:Variable.RedLp ="Off";
    }
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$AOutgoingCall_dssKey] = Press;
    wait:$hold_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A CONN
    set:Variable.Usr = $UserA;set:Variable.State = "CONN";set:Variable.PType = $TypeA;set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B CONN
    set:Variable.Usr = $UserB;set:Variable.State = "CONN";set:Variable.PType = $TypeB;set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $BIncomingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
    set:User($UserB).cm_extn.OnHook;
    wait:$hold_time;

    // User A , B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMESIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMESIdle;

    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = $TypeA;set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = $TypeB;set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $BIncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    wait:$test_delay;

    report:(***** FINISHED Test Internal Calls on Hold ******):<null>;
}

/////////////////////////////////////////////////
// Calls on Hold - External Calls              //
/////////////////////////////////////////////////
TestExternalCallsOnHold:
{
    report:(***** START Test External Calls on Hold ******):<null>;

    wait:$delay_time;

    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = $TypeA;set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = $TypeB;set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $BIncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A offhook
    set:User($UserA).cm_extn.DCP.DSS[$AOutgoingCall_dssKey] = Press;
    wait:$delay_time;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // User A DIAL
    set:Variable.Usr = $UserA;set:Variable.State = "DIAL";set:Variable.PType = $TypeA;set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // A dials B
    set:User($UserA).cm_extn.DialWithGaps.1000=$IPOExtn1;
    wait:$ring_time;

    // User B RINGING and User A RINGBACK
    sync($sync_delay_time_time):User($UserB).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time_time):User($UserA).cm_extn.current_ep.state=CMCSRingBack;

    // User A RINGBACK
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RINGBACK_CALL";set:Variable.PType = $TypeA;set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B RING
    set:Variable.Usr = $UserB;set:Variable.State = "EXT_RING_EXTERNAL";set:Variable.PType = $TypeB;set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $BIncomingCall_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B Answers
    set:User($UserB).cm_extn.DCP.DSS[$BIncomingCall_dssKey] = Press;
    wait:$delay_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A CONN
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CALLED_CONN";set:Variable.PType = $TypeA;set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B CONN
    set:Variable.Usr = $UserB;set:Variable.State = "EXT_CONN_EXTERNAL";set:Variable.PType = $TypeB;set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $BIncomingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    set:Variable.Usr = $UserA; set:Variable.PType = $TypeA;
    gosub:PressHOLDKey;  // push Hold button
    wait:$wait_time;

    verify:User($UserA).cm_extn.state = CMESIdle;
    verify:User($UserB).cm_extn.state = CMESConnected;

    set:Variable.Usr = $UserA;set:Variable.State = "HOLD";set:Variable.PType = $TypeA;set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="Flush";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    set:Variable.Usr = $UserB;set:Variable.State = "EXT_CONN_EXTERNAL";set:Variable.PType = $TypeB;set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $BOutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Wink";
   // if( $PType == "ETR" ):
   // {
   //     set:Variable.GreenLp ="On";
   //     set:Variable.RedLp ="Off";
   // }
    gosub:CheckLamps;
    report:(***** Adrian1 ******):<null>;

    wait:$connect_time;
    wait:$connect_time;
    wait:$connect_time;

    // User A RINGING and User A CONNECTED
    sync($sync_delay_time_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    set:Variable.Usr = $UserA;set:Variable.State = "BACKCALLEXTN";set:Variable.PType = $TypeA;set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="Flush";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    set:Variable.Usr = $UserB;set:Variable.State = "EXT_CONN_EXTERNAL";set:Variable.PType = $TypeB;set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $BOutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Wink";
   // if( $PType == "ETR" ):
   // {
   //     set:Variable.GreenLp ="On";
   //     set:Variable.RedLp ="Off";
   // }
    gosub:CheckLamps;
    report:(***** Adrian2 ******):<null>;

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$AOutgoingCall_dssKey] = Press;
    wait:$hold_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A CONN
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CALLED_CONN";set:Variable.PType = $TypeA;set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B CONN
    set:Variable.Usr = $UserB;set:Variable.State = "EXT_CONN_EXTERNAL";set:Variable.PType = $TypeB;set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $BIncomingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
    set:User($UserB).cm_extn.OnHook;
    wait:$hold_time;

    // User A , B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMESIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMESIdle;

    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = $TypeA;set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $AOutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = $TypeB;set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $BIncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    wait:$test_delay;

    report:(***** FINISHED Test External Calls on Hold ******):<null>;
}

/////////////////////////////////////////////////////////////////////////////

Configuration:
{
    report(*** Started doing phone configuration for test no: $TestID ***):<null>;

    // Internal Calls
    // ETR phones
    if( $TestID == 1 ):
    {
        set:Variable.UserA = $x10_UserName; // ETR18D
        set:Variable.UserB = $x11_UserName; // ETR34D
        set:Variable.ExtnA = $x10_UserNum;
        set:Variable.ExtnB = $x11_UserNum;
        set:Variable.TypeA = $x10_PhoneType;
        set:Variable.TypeB = $x11_PhoneType;
        set:Variable.AIncomingCall_dssKey=1;
        set:Variable.AOutgoingCall_dssKey=0;
        set:Variable.BIncomingCall_dssKey=1;
        set:Variable.BOutgoingCall_dssKey=0;
        if( $CallExtern == 1):
        {
            set:Variable.IPOExtn1 = 201;
            set:Variable.IPOExtn2 = 202;
            set:Variable.AIncomingCall_dssKey=5;
            set:Variable.AOutgoingCall_dssKey=4;
            set:Variable.BIncomingCall_dssKey=5;
            set:Variable.BOutgoingCall_dssKey=4;
        }
    }
    // 14xx phones
    if( $TestID == 2 ):
    {
        set:Variable.UserA = $x20_UserName; // 1408
        set:Variable.UserB = $x19_UserName; // 1416
        set:Variable.ExtnA = $x20_UserNum;
        set:Variable.ExtnB = $x19_UserNum;
        set:Variable.TypeA = $x20_PhoneType;
        set:Variable.TypeB = $x19_PhoneType;
        set:Variable.AIncomingCall_dssKey=5;
        set:Variable.AOutgoingCall_dssKey=4;
        set:Variable.BIncomingCall_dssKey=14;
        set:Variable.BOutgoingCall_dssKey=15;
        if( $CallExtern == 1):
        {
            set:Variable.IPOExtn1 = 201;
            set:Variable.IPOExtn2 = 202;
            set:Variable.AIncomingCall_dssKey=1;
            set:Variable.AOutgoingCall_dssKey=0;
            set:Variable.BIncomingCall_dssKey=10;
            set:Variable.BOutgoingCall_dssKey=11;
        }
    }
    // 95xx phones
    if( $TestID == 3 ):
    {
        set:Variable.UserA = $x18_UserName;  // 9500
        set:Variable.UserB = $x19_UserName;  // 1416
        set:Variable.ExtnA = $x18_UserNum;
        set:Variable.ExtnB = $x19_UserNum;
        set:Variable.TypeA = $x18_PhoneType;
        set:Variable.TypeB = $x19_PhoneType;
        set:Variable.AIncomingCall_dssKey=1;
        set:Variable.AOutgoingCall_dssKey=0;
        set:Variable.BIncomingCall_dssKey=14;
        set:Variable.BOutgoingCall_dssKey=15;
        if( $CallExtern == 1):
        {
            set:Variable.IPOExtn1 = 201;
            set:Variable.IPOExtn2 = 202;
            set:Variable.AIncomingCall_dssKey=5;
            set:Variable.AOutgoingCall_dssKey=4;
            set:Variable.BIncomingCall_dssKey=10;
            set:Variable.BOutgoingCall_dssKey=11;
        }
    }
    // 95xx phones
    if( $TestID == 4 ):
    {
        set:Variable.UserA = $x19_UserName;  // 1400
        set:Variable.UserB = $x18_UserName;  // 9500
        set:Variable.ExtnB = $x18_UserNum;
        set:Variable.ExtnA = $x19_UserNum;
        set:Variable.TypeB = $x18_PhoneType;
        set:Variable.TypeA = $x19_PhoneType;
        set:Variable.BIncomingCall_dssKey=1;
        set:Variable.BOutgoingCall_dssKey=0;
        set:Variable.AIncomingCall_dssKey=14;
        set:Variable.AOutgoingCall_dssKey=15;
        if( $CallExtern == 1):
        {
            set:Variable.IPOExtn1 = 201;
            set:Variable.IPOExtn2 = 202;
            set:Variable.AIncomingCall_dssKey=10;
            set:Variable.AOutgoingCall_dssKey=11;
            set:Variable.BIncomingCall_dssKey=5;
            set:Variable.BOutgoingCall_dssKey=4;
        }
    }
}

Deconfiguration:
{
    report(*** Started doing phone deconfiguration for test no: $TestID ***):<null>;

    set:Variable.UserA = Extn;
    set:Variable.UserB = Extn;
    set:Variable.UserC = Extn;
    set:Variable.UserD = Extn;
    set:Variable.ExtnA = Extn;
    set:Variable.ExtnB = Extn;
    set:Variable.ExtnC = Extn;
    set:Variable.ExtnD = Extn;
    set:Variable.IncomingCall_dssKey=0;
    set:Variable.OutgoingCall_dssKey=0;
    set:Variable.AIncomingCall_dssKey=0;
    set:Variable.AOutgoingCall_dssKey=0;
    set:Variable.BIncomingCall_dssKey=0;
    set:Variable.BOutgoingCall_dssKey=0;
    set:Variable.IPOExtn1 = 0;
    set:Variable.IPOExtn2 = 0;

    report(*** Finished doing phone deconfiguration for test no: $TestID ***):<null>;
}

//////////////////////  CHECK LAMPS ////////////////////////////////////////////
CheckLamps:
{
    report(*** STARTED: Lamps verification for User: $Usr ***):<null>;
    report(*** Button: $Btn ***):<null>;
    report(*** Green Lamp: $GreenLp ***):<null>;
    report(*** Red Lamp: $RedLp ***):<null>;

    // GREEN LAMP VERIFICATION
    if( $GreenLp == Off ):
    {
        verify(Lamp Verification Issue: GreenLamp of $Btn button of USER=$Usr is not Off):User($Usr).cm_extn.DCP.DSS[$Btn].GreenLamp= Off;
    }
    if( $GreenLp == On ):
    {
        verify(Lamp Verification Issue: GreenLamp of $Btn button of USER=$Usr is not On):User($Usr).cm_extn.DCP.DSS[$Btn].GreenLamp= On;
    }
    if( $GreenLp == Flash ):
    {
        verify(Lamp Verification Issue: GreenLamp of $Btn button of USER=$Usr is not Flashing):User($Usr).cm_extn.DCP.DSS[$Btn].GreenLamp= Flash;
    }
    if( $GreenLp == Wink ):
    {
        verify(Lamp Verification Issue: GreenLamp of $Btn button of USER=$Usr is not Winking):User($Usr).cm_extn.DCP.DSS[$Btn].GreenLamp= Wink;
    }


    // RED LAMP VERIFICATION
    if( $RedLp == Off ):
    {
        verify(Lamp Verification Issue: RedLamp of $Btn button of USER=$Usr is not Off):User($Usr).cm_extn.DCP.DSS[$Btn].RedLamp = Off;
    }
    if( $RedLp == On ):
    {
        verify(Lamp Verification Issue: RedLamp of $Btn button of USER=$Usr is not On):User($Usr).cm_extn.DCP.DSS[$Btn].RedLamp = On;
    }
    if( $RedLp == Flash ):
    {
        verify(Lamp Verification Issue: RedLamp of $Btn button of USER=$Usr is not Flashing):User($Usr).cm_extn.DCP.DSS[$Btn].RedLamp = Flash;
    }
    if( $RedLp == Wink ):
    {
        verify(Lamp Verification Issue: RedLamp of $Btn button of USER=$Usr is not Winking):User($Usr).cm_extn.DCP.DSS[$Btn].RedLamp = Wink;
    }

    report(*** FINISHED: Lamps verification for User: $Usr ***):<null>;
}

///////////////////// CHECK DISPLAYS //////////////////////////////////////////////////
CheckDisplay:
{
    report(*** STARTED: Display verification for User: $Usr ***):<null>;

    report(*** State checked : $State ***):<null>;
    report(*** Phone Type: $PType ***):<null>;
    report(*** Other Extn: $OtherExtn ***):<null>;

    // PLEASE NOTE: User, State, OtherExtn and PhoneType must be set before running this rutine

    // IDLE
    if( $State == "IDLE" ):
    {
        report(** IDLE ***):<null>;
        if( $PType == "ETR" ):
        {
            report(*** ETR phone - do not check IDLE display ***):<null>;
        }
        if( $PType == "1508" ):
        {
            set:Variable.l1="        Feature  Admin  ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for IDLE screen on line 3 ):User($Usr).cm_extn.DCP.Display[2]=$l1;
        }
        if( $PType == "1516" ):
        {
            set:Variable.l2="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for IDLE screen on line 4 ):User($Usr).cm_extn.DCP.Display[3]=$l2;
        }
        if( $PType == "9508"):
        {
            set:Variable.line2="                        ";
            set:Variable.line3="                        ";
            set:Variable.line4="Intercom 1              ";
            set:Variable.line5="Intercom 2              ";
            set:Variable.line6="Line 01                 ";
            set:Variable.line7="Line 02                 ";
            //set:Variable.lineX="Redial      Featu Admin "; //"            Featu Admin ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for IDLE screen on line 2 ):User($Usr).cm_extn.DCP.Display[3]=$line4;
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for IDLE screen on line 3 ):User($Usr).cm_extn.DCP.Display[4]=$line5;
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for IDLE screen on line 4 ):User($Usr).cm_extn.DCP.Display[3]=$line4;
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for IDLE screen on line 5 ):User($Usr).cm_extn.DCP.Display[4]=$line5;
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for IDLE screen on line 6 ):User($Usr).cm_extn.DCP.Display[5]=$line6;
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for IDLE screen on line 7 ):User($Usr).cm_extn.DCP.Display[6]=$line7;
            //verify(Display Verification Issue: 9508 User: $Usr has incorrect info for IDLE screen on line 12 ):User($Usr).cm_extn.DCP.Display[11]=$lineX;
        }
    }
    // DIAL = user going offhook from IDLE state
    if( $State == "DIAL" ):
    {
        report(** DIAL ***):<null>;
        if( $PType == "ETR" ):
        {
            // check only first line is empty
            set:Variable.line0="                        ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for DIAL screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line0;

        }
        if( $PType == "1508" ):
        {
            set:Variable.line1="Dial: Number?           ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for DIAL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for DIAL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="        Feature         ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for DIAL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
        }
        if( $PType == "1516" ):
        {
            set:Variable.line1="Dial: Number?           ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for DIAL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for DIAL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for DIAL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
            set:Variable.line4="        Feature         ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for DIAL screen on line 3):User($Usr).cm_extn.DCP.Display[3]=$line4;
        }
        if($PType == "9508"):
        {
            set:Variable.line2="Dial: Number?           ";
            set:Variable.line3="                        ";
            set:Variable.line6="Line 01                 ";
            set:Variable.line7="Line 02                 ";
            //set:Variable.lineX="Redial             Drop ";
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for DIAL screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line2;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for DIAL screen on line 3 ):User($Usr).cm_extn.DCP.Display[2]=$line3;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for DIAL screen on line 6 ):User($Usr).cm_extn.DCP.Display[5]=$line6;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for DIAL screen on line 7 ):User($Usr).cm_extn.DCP.Display[6]=$line7;
            //verify(Display Verification Issue: 9500 User: $Usr has incorrect info for DIAL screen on line 12 ):User($Usr).cm_extn.DCP.Display[11]=$lineX;
        }
    }
    // RING - State associated to user ringing when it is being called from an internal extension
    if( $State == "RING" ):
    {
        report(** RING ***):<null>;
        if( $PType == "ETR" ):
        {
            set:Variable.line1="$OtherExtn                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for RING screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="                        ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for RING screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line2;

        }
        if( $PType == "1508" ):
        {
            set:Variable.line1="Call: Incoming          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RING screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            //set:Variable.line2="o%$OtherExtn             ";
            //verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RING screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="         To VM   Ignore ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RING screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
        }
        if( $PType == "1516" ):
        {
            set:Variable.line1="Call: Incoming          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RING screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="o%$OtherExtn             ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RING screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RING screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
            set:Variable.line4="         To VM   Ignore ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RING screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$line4;
        }
        if($PType == "9508"):
        {
            set:Variable.line2="Incoming: $OtherExtn    ";
            set:Variable.line3="$OtherExtn              ";
            set:Variable.line6="Line 01                 ";
            set:Variable.line7="Line 02                 ";
            set:Variable.lineX="Answe To VM Ignore Drop ";
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line2;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 3 ):User($Usr).cm_extn.DCP.Display[2]=$line3;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 6 ):User($Usr).cm_extn.DCP.Display[5]=$line6;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 7 ):User($Usr).cm_extn.DCP.Display[6]=$line7;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 12 ):User($Usr).cm_extn.DCP.Display[11]=$lineX;
        }
    }
    // EXT_RING_EXTERNAL - State associated to user ringing when it is being called from an external extension over PRI/T1 Trunk
    if( $State == "EXT_RING_EXTERNAL" ):
    {
        report(** EXT_RING_EXTERNAL ***):<null>;
        if( $PType == "ETR" ):
        {
            set:Variable.line0="External              ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line0;
            set:Variable.line0="                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line0;
        }
        if( $PType == "1508" ):
        {
            set:Variable.line0="Call: Incoming          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line0;
            set:Variable.line0="o%External              ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line0;
            set:Variable.line0="                 Ignore ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line0;
        }
        if( $PType == "1516" ):
        {
            set:Variable.line0="Call: Incoming          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line0;
            set:Variable.line0="o%External              ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line0;
            set:Variable.line0="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line0;
            set:Variable.line0="                 Ignore ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$line0;
        }
        if($PType == "9508"):
        {
            set:Variable.line2="Incoming:";
            set:Variable.line3="External                ";
            set:Variable.line6="Line 01                 ";
            set:Variable.line7="Line 02                 ";
            set:Variable.lineX="Answer      Ignore Drop ";
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line2;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 3 ):User($Usr).cm_extn.DCP.Display[2]=$line3;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 6 ):User($Usr).cm_extn.DCP.Display[5]=$line6;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 7 ):User($Usr).cm_extn.DCP.Display[6]=$line7;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 12 ):User($Usr).cm_extn.DCP.Display[11]=$lineX;
        }
    }
    //RINGBACK - State associated to user calling another internal extension
    if( $State == "RINGBACK" ):
    {
        report(** RINGBACK ***):<null>;
        if( $PType == "ETR" ):
        {
            set:Variable.line0="$OtherExtn                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for RINGBACK screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line0;
        }
        if( $PType == "1508" ):
        {
            set:Variable.line1="Call:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RINGBACK screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="v|$OtherExtn            ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RINGBACK screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3=" AutCB                  ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RINGBACK screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
        }
        if( $PType == "1516" ):
        {
            set:Variable.line1="Call:                   ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RINGBACK screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="v|$OtherExtn            ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RINGBACK screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RINGBACK screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
            set:Variable.line4=" AutCB                  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RINGBACK screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$line4;
        }
        if($PType == "9508"):
        {
            set:Variable.line2="Calling:";
            set:Variable.line3="$OtherExtn              ";
            set:Variable.line6="Line 01                 ";
            set:Variable.line7="Line 02                 ";
            set:Variable.lineX="CallBa             Drop ";
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line2;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 3 ):User($Usr).cm_extn.DCP.Display[2]=$line3;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 6 ):User($Usr).cm_extn.DCP.Display[5]=$line6;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 7 ):User($Usr).cm_extn.DCP.Display[6]=$line7;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 12 ):User($Usr).cm_extn.DCP.Display[11]=$lineX;
        }
    }
    //EXT_RINGBACK_CALL - State associated to user calling an external extension over PRI/T1 Trunk
    if( $State == "EXT_RINGBACK_CALL" ):
    {
        report(** EXT_RINGBACK_CALL ***):<null>;

        if( $PType == "ETR" ):
        {
            set:Variable.line0="$OtherExtn                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line0;
        }
        if( $PType == "1508" ):
        {
            set:Variable.line1="Call:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="o|$OtherExtn            ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="                        ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
        }
        // not verified - to be rebuilt
        if( $PType == "1516" ):
        {
            set:Variable.line1="Call:                   ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="o|$OtherExtn    ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
            set:Variable.line4="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$line4;
        }
        if($PType == "9508"):
        {
            set:Variable.line2="Calling:";
            set:Variable.line3="$OtherExtn              ";
            set:Variable.line6="Line 01                 ";
            set:Variable.line7="Line 02                 ";
            set:Variable.lineX="                   Drop ";
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line2;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 3 ):User($Usr).cm_extn.DCP.Display[2]=$line3;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 6 ):User($Usr).cm_extn.DCP.Display[5]=$line6;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 7 ):User($Usr).cm_extn.DCP.Display[6]=$line7;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for RING screen on line 12 ):User($Usr).cm_extn.DCP.Display[11]=$lineX;
        }
    }
    //CONN - State associated to user connected to another internal extension
    if( $State == "CONN" ):
    {
        report(** CONN ***):<null>;
        if( $PType == "ETR" ):
        {

            set:Variable.line0="$OtherExtn                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for CONN screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line0;
        }
        if( $PType == "1508" ):
        {
            set:Variable.line1="Conn:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CONN screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            //set:Variable.line2="o|                      ";
            //verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CONN screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="$OtherExtn                    >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CONN screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
        }
        if( $PType == "1516" ):
        {
            set:Variable.line1="Conn:                  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONN screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            //set:Variable.line2="v|                     ";
            //verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONN screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="$OtherExtn             ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONN screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
            set:Variable.line4="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONN screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$line4;
        }
        if($PType == "9508"):
        {
            set:Variable.line2="Connected: $OtherExtn";
            set:Variable.line3="                        ";
            set:Variable.line6="Line 01                 ";
            set:Variable.line7="Line 02                 ";
            set:Variable.lineX=" Hold  Conf Transf Drop ";
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line2;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 3 ):User($Usr).cm_extn.DCP.Display[2]=$line3;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 6 ):User($Usr).cm_extn.DCP.Display[5]=$line6;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 7 ):User($Usr).cm_extn.DCP.Display[6]=$line7;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 12 ):User($Usr).cm_extn.DCP.Display[11]=$lineX;
        }
    }
    //EXT_CONN_EXTERNAL - State associated to user connected to an external extension over PRI/T1 Trunk
    if( $State == "EXT_CONN_EXTERNAL" ):
    {
        report(** EXT_CONN_EXTERNAL ***):<null>;

        if( $PType == "ETR" ):
        {
            set:Variable.line0="External";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line0;
        }
        // not verified - to be rebuilt
        if( $PType == "1508" ):
        {
            set:Variable.line1="Conn:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="o|External        ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="        Feature  Admin  ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
        }
        if( $PType == "1516" ):
        {
            set:Variable.line1="Conn:            ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="o|External        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
            set:Variable.line4="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$line4;
        }
        if($PType == "9508"):
        {
            set:Variable.line2="Connected:";
            set:Variable.line3="External                ";
            set:Variable.line6="Line 01                 ";
            set:Variable.line7="Line 02                 ";
            set:Variable.lineX=" Hold  Conf Transf Drop ";
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line2;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 3 ):User($Usr).cm_extn.DCP.Display[2]=$line3;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 6 ):User($Usr).cm_extn.DCP.Display[5]=$line6;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 7 ):User($Usr).cm_extn.DCP.Display[6]=$line7;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 12 ):User($Usr).cm_extn.DCP.Display[11]=$lineX;
        }
    }
    //HOLD - State associated to user who puts on hold another internal user
    if( $State == "HOLD" ):
    {
        report(** HOLD ***):<null>;
        // not verified - to be rebuilt
        if( $PType == "ETR" ):
        {
            set:Variable.line0="";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for HOLD screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line0;
        }
        if( $PType == "1508" ):
        {
            set:Variable.line1="Call: On-Hold           ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HOLD screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            //set:Variable.line2="v";
            //verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HOLD screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="$OtherExtn                    >>";
            if( $CallExtern == 1):
            {
                set:Variable.line3="$OtherExtn                   >>";
            }
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HOLD screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
        }
        if( $PType == "1516" ):
        {
            set:Variable.line1="Call: On-Hold           ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HOLD screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            //set:Variable.line2="o";
            //verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HOLD screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HOLD screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
            set:Variable.line4=" Pickup             ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HOLD screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$line4;
        }
        if($PType == "9508"):
        {
            set:Variable.line2="On-Hold: $OtherExtn";
            set:Variable.line3="                        ";
            if( $CallExtern == 1):
            {
                set:Variable.line3="External                ";
            }
            set:Variable.line6="Line 01                 ";
            set:Variable.line7="Line 02                 ";
            set:Variable.lineX="Connec Conf Transf      ";
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line2;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 3 ):User($Usr).cm_extn.DCP.Display[2]=$line3;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 6 ):User($Usr).cm_extn.DCP.Display[5]=$line6;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 7 ):User($Usr).cm_extn.DCP.Display[6]=$line7;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 12 ):User($Usr).cm_extn.DCP.Display[11]=$lineX;
        }
    }
    //HELD - State associated to user who is put on hold by another internal user
    if( $State == "HELD" ):
    {
        report(** HELD ***):<null>;
        // not verified - to be rebuilt
        if( $PType == "ETR" ):
        {
            set:Variable.line0="$OtherExtn";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for HELD screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line0;
        }
        if( $PType == "1508" ):
        {
            set:Variable.line1="Held:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HELD screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            //set:Variable.line2="v";
            //verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HELD screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="$OtherExtn                    >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HELD screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
        }
        if( $PType == "1516" ):
        {
            set:Variable.line1="Held:                  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HELD screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            //set:Variable.line2="o|                      ";
            //verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HELD screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HELD screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
            set:Variable.line4="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HELD screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$line4;
        }
        if($PType == "9508"):
        {
            set:Variable.line2="Held: $OtherExtn";
            set:Variable.line3="                        ";
            set:Variable.line6="Line 01                 ";
            set:Variable.line7="Line 02                 ";
            set:Variable.lineX=" Hold  Conf Transf Drop ";
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line2;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 3 ):User($Usr).cm_extn.DCP.Display[2]=$line3;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 6 ):User($Usr).cm_extn.DCP.Display[5]=$line6;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 7 ):User($Usr).cm_extn.DCP.Display[6]=$line7;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 12 ):User($Usr).cm_extn.DCP.Display[11]=$lineX;
        }
    }
    //BACKCALL - State associated to user who is called back by another internal user who is put on hold
    if( $State == "BACKCALL" ):
    {
        report(** BACKCALL ***):<null>;

        if( $PType == "ETR" ):
        {
            set:Variable.line1="<$OtherExtn";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for BACKCALL screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="$OtherExtn";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for BACKCALL screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line2;
        }
        if( $PType == "1508" ):
        {
            set:Variable.line1="Call: Incoming          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for BACKCALL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            //set:Variable.line2="o%$OtherExtn             ";
            //verify(Display Verification Issue: 1508 User: $Usr has incorrect info for BACKCALL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="$OtherExtn                    >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for BACKCALL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
        }
        if( $PType == "1516" ):
        {
            set:Variable.line1="Call: Incoming          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for BACKCALL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            //set:Variable.line2="o%$OtherExtn             ";
            //verify(Display Verification Issue: 1516 User: $Usr has incorrect info for BACKCALL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for BACKCALL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
            set:Variable.line4="                 Ignore ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for BACKCALL screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$line4;
        }
        if($PType == "9508"):
        {
            set:Variable.line2="Incoming: $OtherExtn";
            set:Variable.line3="<$OtherExtn             ";
            set:Variable.line6="Line 01                 ";
            set:Variable.line7="Line 02                 ";
            set:Variable.lineX="Answer      Ignore Drop ";
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line2;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 3 ):User($Usr).cm_extn.DCP.Display[2]=$line3;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 6 ):User($Usr).cm_extn.DCP.Display[5]=$line6;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 7 ):User($Usr).cm_extn.DCP.Display[6]=$line7;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 12 ):User($Usr).cm_extn.DCP.Display[11]=$lineX;
        }
    }
    //HOLD Call Back External - State associated to user who is called back by another external user who is put on hold
    if( $State == "BACKCALLEXTN" ):
    {
        report(** BACKCALLEXTN ***):<null>;

        if( $PType == "ETR" ):
        {
            set:Variable.line1="<External               ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for BACKCALL screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="$OtherExtn";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for BACKCALL screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line2;
        }
        if( $PType == "1508" ):
        {
            set:Variable.line1="Call: Incoming          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for BACKCALL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            //set:Variable.line2="o%$OtherExtn             ";
            //verify(Display Verification Issue: 1508 User: $Usr has incorrect info for BACKCALL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for BACKCALL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
        }
        if( $PType == "1516" ):
        {
            set:Variable.line1="Call: Incoming          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for BACKCALL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            //set:Variable.line2="o%$OtherExtn             ";
            //verify(Display Verification Issue: 1516 User: $Usr has incorrect info for BACKCALL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for BACKCALL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
            set:Variable.line4="                 Ignore ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for BACKCALL screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$line4;
        }
        if($PType == "9508"):
        {
            set:Variable.line2="Incoming: $OtherExtn";
            set:Variable.line3="<External               ";
            set:Variable.line6="Line 01                 ";
            set:Variable.line7="Line 02                 ";
            set:Variable.lineX="Answer      Ignore Drop ";
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line2;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 3 ):User($Usr).cm_extn.DCP.Display[2]=$line3;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 6 ):User($Usr).cm_extn.DCP.Display[5]=$line6;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 7 ):User($Usr).cm_extn.DCP.Display[6]=$line7;
            verify(Display Verification Issue: 9500 User: $Usr has incorrect info for CONN screen on line 12 ):User($Usr).cm_extn.DCP.Display[11]=$lineX;
        }
    }

    report(*** FINISHED: Display verification for User: $Usr ***):<null>;
}

////////////////////// MAPDSSKEY /////////////////////////////////////////////
PressSoftKey1:
{
    report(PressSoftKey1):<null>;
    set:User($Usr).cm_extn.DCP.MenuKey = A;
}

PressSoftKey2:
{
    report(PressSoftKey2):<null>;
    set:User($Usr).cm_extn.DCP.MenuKey = B;
}

PressSoftKey3:
{
    report(PressSoftKey3):<null>;
    set:User($Usr).cm_extn.DCP.MenuKey = C;
}

PressSoftKey4:
{
    report(PressSoftKey4):<null>;
    set:User($Usr).cm_extn.DCP.MenuKey = I;
}

PressHOLDKey:
{
    report(PressHOLDKey):<null>;

    if( $PType == "ETR" ):
    {
        set:User($Usr).cm_extn.DCP.FeatureKey = DCPLFeatureHold;  // push Hold button
        wait:$wait_time;
    }
    if( $PType == "1508" ):
    {
        set:User($Usr).cm_extn.DCP.FeatureKey = DCPLFeatureHold;  // push Hold button
        wait:$wait_time;
    }
    if( $PType == "1516" ):
    {
        set:User($Usr).cm_extn.DCP.FeatureKey = DCPLFeatureHold;  // push Hold button
        wait:$wait_time;
    }
    if( $PType == "9508" ):
    {
        gosub:PressSoftKey1;  // push Hold button
        wait:$wait_time;
    }
}

Offhook:
{
    set:User($Usr).cm_extn.DCP.DSS[$OutgoingCall_dssKey] = Press;
    sync($sync_delay_time):User($Usr).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;
}

///////////////////////////////////////////////////////////////////////////////
User1dialsUser2:
{
    // 1 dials 2
    set:User($User1).cm_extn.DialWithGaps.1000=$Extn2;
    wait:$wait_time;

    // User 2 ringing, 1 ringback
    sync($sync_delay_time_time):User($User2).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time_time):User($User1).cm_extn.current_ep.state=CMCSRingBack;

    // User B Answers
    //set:User($User2).cm_extn.DCP.DSS[$IncomingCall_dssKey] = Press;
    set:User($User2).cm_extn.DCP.HookChange = OffHook;
    wait:$wait_time;  //wait:$connect_time;

    // User 1 and User 2 connected
    sync($sync_delay_time):User($User1).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($User2).cm_extn.current_ep.state=CMCSConnected;

    // Talkpath between 1 & 2
    sync($sync_delay_time):User($User2).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($User2).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($User1).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($User1).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
}

///////////////////////////////////////////////////////////////////////////////
User1ringsUser2:
{
    set:Variable.UserName = $User2;
    gosub:PressExit;
    set:Variable.UserName = $User1;
    gosub:PressExit;

    gosub:Offhook;

    gosub:User1dialsUser2;
}
///////////////////////////////////////////////////////////////////////////////
UserAdialsUserB:
{
        set:Variable.ExternalCall = false;
    // User A offhook
    set:User($UserA).cm_extn.DCP.DSS[$IntOutCall_dssKey] = Press;
    sync($screen_sync_delay_time_time):User($UserA).cm_extn.current_ep.state=CMCSDialling;
    verify(Tone Verification Issue: $UserA is not in dialing state):User($UserA).cm_extn.current_ep.state=CMCSDialling;

    set:User($UserA).cm_extn.DialWithGaps.1000= $ExtnB;

    wait:4000;

    // User A&C are ringing
    sync($screen_sync_delay_time_time):User($UserB).cm_extn.current_ep.state=CMCSRinging;
    verify(Tone Verification Issue: $UserB is not alerting):User($UserB).cm_extn.current_ep.state=CMCSRinging;
    sync($screen_sync_delay_time_time):User($UserA).cm_extn.current_ep.state=CMCSRingBack;
    verify(Tone Verification Issue: $UserA is not ringback):User($UserA).cm_extn.current_ep.state=CMCSRingBack;
}

///////////////////////////////////////////////////////////////////////////////
UserCdialsUserD:
{
    // User C offhook
    set:User($UserC).cm_extn.DCP.DSS[$DialButtonC] = Press;
    sync($screen_sync_delay_time_time):User($UserC).cm_extn.current_ep.state=CMCSDialling;
    verify(Tone Verification Issue: $UserC is not in dialing state):User($UserC).cm_extn.current_ep.state=CMCSDialling;

    set:User($UserC).cm_extn.DialWithGaps.1000= $ExtnD;

    wait:2000;

    // User is ringing
    sync($screen_sync_delay_time_time):User($UserD).cm_extn.current_ep.state=CMCSRinging;
    verify(Tone Verification Issue: $UserD is not alerting):User($UserD).cm_extn.current_ep.state=CMCSRinging;
    sync($screen_sync_delay_time_time):User($UserC).cm_extn.current_ep.state=CMCSRingBack;
    verify(Tone Verification Issue: $UserA is not ringback):User($UserC).cm_extn.current_ep.state=CMCSRingBack;
}
//Simulation of call coming from external trunk.
TrunkTo14xxphone:
{
    set:Variable.ExternalCall = true;
    if($RunMode == Rig):
    {
        // User A offhook
        //set:User($UserA).cm_extn.DCP.HookChange = OffHook;
        set:User($UserA).cm_extn.DCP.DSS[$OutgoingCall_dssKey] = Press;
        sync($screen_sync_delay_time_time):User($UserA).cm_extn.current_ep.state=CMCSDialling;
        verify(Tone Verification Issue: $UserA is not in dialing state):User($UserA).cm_extn.current_ep.state=CMCSDialling;

        // A dials external number
        set:User($UserA).cm_extn.DialWithGaps.1500 = $ExternalNr;
    }
    if($RunMode == Simulator):
    {
        gosub:MakeICAlogTrunkCall;
    }
    wait:9000;

    // User B is ringing
    sync($screen_sync_delay_time_time):User($UserB).cm_extn.current_ep.state=CMCSRinging;
    verify(Tone Verification Issue: $UserB is not alerting):User($UserB).cm_extn.current_ep.state=CMCSRinging;
    //sync($screen_sync_delay_time_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    //verify(Tone Verification Issue: $UserA is not connected):User($UserA).cm_extn.current_ep.state=CMCSConnected;
}

MapDssKeys:
{
    if($PhoneType == 1508):
    {
        if($dssKey < 4):
        {
                set:Variable.dssKey = $dssKey+4;
        }
        else:
        {
                set:Variable.dssKey = $dssKey-4;
        }
    }
    if($PhoneType == 1516):
    {
        if($dssKey==0):
        {
            set:Variable.dssKey  = 15;
        }
        if($dssKey==1):
        {
            set:Variable.dssKey  = 14;
        }
        if($dssKey==2):
        {
            set:Variable.dssKey  = 13;
        }
        if($dssKey==3):
        {
            set:Variable.dssKey  = 12;
        }
        if($dssKey==4):
        {
            set:Variable.dssKey  = 11;
        }
        if($dssKey==5):
        {
            set:Variable.dssKey  = 10;
        }
        if($dssKey==6):
        {
            set:Variable.dssKey  = 9;
        }
        if($dssKey==7):
        {
           set:Variable.dssKey  = 8;
        }
        if($dssKey==8):
        {
            set:Variable.dssKey  = 7;
        }
        if($dssKey==9):
        {
            set:Variable.dssKey  = 6;
        }
        if($dssKey==10):
        {
            set:Variable.dssKey  = 5;
        }
        if($dssKey==11):
        {
            set:Variable.dssKey  = 4;
        }
        if($dssKey==12):
        {
            set:Variable.dssKey  = 3;
        }
        if($dssKey==13):
        {
            set:Variable.dssKey  = 2;
        }
        if($dssKey==14):
        {
            set:Variable.dssKey  = 1;
        }
        if($dssKey==15):
        {
            set:Variable.dssKey  = 0;
        }
    }
}

//Put phone on hook
UserOnHook:
{
        set:User($Usr).cm_extn.OnHook;
        //set:User($Usr).cm_extn.DCP.DSS[$OutgoingCall_dssKey] = Press;
        wait:$lamptime;
   // User idle
    sync($sync_delay_time):User($Usr).cm_extn.state=CMESIdle;
    verify(Tone Verification Issue: $Usr is not idle):User($Usr).cm_extn.state=CMESIdle;
    // User IDLE
        set:Variable.State = "IDLE";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
}
