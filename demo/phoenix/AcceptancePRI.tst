////////////////////////////////////////////////////////////////////////////////
// ----------------------------------------------------------------------------
// ..\..\Partner\AcceptancePRI.tst
//
// Script for Partner Acceptance run against PRI configurations
//
// Duration to run on target: 25min
//
// Modification History
// YYMMDD Name                    Comment
// 110124 Mihai Manolache         Initial Creation
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
    set:Variable.sync_delay_time = 15000;
    set:Variable.wait_time = 1000;
    set:Variable.connect_time=10000;
    set:Variable.ring_time=15000;
    set:Variable.ring_time_POTS=15000;
    set:Variable.transfer_ring_time=5000;
    set:Variable.idle_time=5000;
    set:Variable.VM_connect_time=20000;
    set:Variable.hold_time=5000;
    set:Variable.test_delay=10000;

    /////////////////////////////////////////////////////////////////////////
    ///////// Workaround for Voicemail not starting up quickly///////////////
    /////////////////////////////////////////////////////////////////////////
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
    set:Variable.TestID=1;
    set:Variable.TestEnd=29;
    while($TestID <= $TestEnd):
    {
        gosub:TestCase$TestID;
        set:Variable.TestID = $TestID + 1;
        wait:$wait_time;
    }
}

///////////////////////////////////////////////////////////////////////////////
/////////////////////        ACCEPTANCE TESTS        //////////////////////////
///////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////
// Acceptance - TestCase1                                               //
//    SCENARIO (2): keywords=Outgoing calls after installation - DFT    //
//    SCENARIO (3): keywords=Incoming answered call after installation  //
//////////////////////////////////////////////////////////////////////////
TestCase1:
{
    report(********** TestCase1 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicUpgrade;
    gosub:Deconfiguration;
    report(********** TestCase1 COMPLETED **********):<null>;
}

/////////////////////////////////////////////////////////////////////
// Acceptance - TestCase2                                          //
//    SCENARIO (4): keywords=Basic Key functionality provides      //
//                  2 Channels for Embedded voicemail              //
//                                                                 //
/////////////////////////////////////////////////////////////////////
TestCase2:
{
    report(********** TestCase2 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicEmbeddedVM;
    gosub:Deconfiguration;
    report(********** TestCase2 COMPLETED **********):<null>;
}

/////////////////////////////////////////////////////////////////////
// Acceptance - TestCase3                                          //
//    SCENARIO (5): keywords=Upgrade from Manager                  //
//    SCENARIO (6): keywords=Upgrade from Manager from the 6.0 GA  //
//    SCENARIO (7): keywords=Upgrade from Optional SD card         //
//                                                                 //
/////////////////////////////////////////////////////////////////////
TestCase3:
{
    report(********** TestCase3 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicFeature;
    gosub:Deconfiguration;
    report(********** TestCase3 COMPLETED **********):<null>;
}

/////////////////////////////////////////////////////////////////////
// Acceptance - TestCase4                                          //
//    SCENARIO (11): keywords=Analogue Trunk – Outgoing call – ETR //
//    SCENARIO (15): keywords=Analogue Trunk – Incoming call – ETR //
//      Originator phone type: ETR(34D)                            //
//      Destination phone type: ETR(18D)                           //
//                                                                 //
/////////////////////////////////////////////////////////////////////
TestCase4:
{
    report(********** TestCase4 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncomingETRCallAnalog;
    gosub:Deconfiguration;
    report(********** TestCase4 COMPLETED **********):<null>;
}

//////////////////////////////////////////////////////////////////////
// Acceptance - TestCase5                                           //
//    SCENARIO (12): keywords=Analogue Trunk – Outgoing call – 14xx //
//    SCENARIO (16): keywords=Analogue Trunk – Incoming call – 14xx //
//      Originator phone type: 14xx                                 //
//      Destination phone type: 14xx                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase5:
{
    report(********** TestCase5 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncoming14XXCallAnalog;
    gosub:Deconfiguration;
    report(********** TestCase5 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - TestCase6                                           //
//    SCENARIO (13): keywords=Analogue Trunk – Outgoing call – POT  //
//    SCENARIO (17): keywords=Analogue Trunk – Incoming call – POT  //
//      Originator phone type: POT                                  //
//      Destination phone type: ETR (call cannot be answered        //
//      correctly by POT)                                           //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase6:
{
    report(********** TestCase6 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncomingPOTCallAnalog;
    gosub:Deconfiguration;
    report(********** TestCase6 COMPLETED **********):<null>;
}
////////////////////////////////////////////////////////////////////////////////
// Acceptance - TestCase7                                                     //
//    SCENARIO (14): keywords=Analogue Trunk – Outgoing call – ETR/POT COMBO  //
//    SCENARIO (18): keywords=Analogue Trunk – Incoming call – ETR/POT COMBO  //
//      Originator phone type: POT CONNECTED TO ETR CARD                      //
//      Destination phone type: ETR (call cannot be answered                  //
//      correctly by POT)                                                     //
//                                                                            //
////////////////////////////////////////////////////////////////////////////////
TestCase7:
{
    report(********** TestCase7 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncomingETRPOTCallAnalog;
    gosub:Deconfiguration;
    report(********** TestCase7 COMPLETED **********):<null>;
}

/////////////////////////////////////////////////////////////////////
// Acceptance - TestCase8                                          //
//    SCENARIO (27): keywords=SIP Trunk – Outgoing call – ETR      //
//    SCENARIO (31): keywords=SIP Trunk – Incoming call – ETR      //
//      Originator phone type: ETR(34D)                            //
//      Destination phone type: ETR(18D)                           //
//                                                                 //
/////////////////////////////////////////////////////////////////////
TestCase8:
{
    report(********** TestCase8 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncomingETRCallSIP;
    gosub:Deconfiguration;
    report(********** TestCase8 COMPLETED **********):<null>;
}

//////////////////////////////////////////////////////////////////////
// Acceptance - TestCase9                                           //
//    SCENARIO (28): keywords=SIP Trunk – Outgoing call – 14xx      //
//    SCENARIO (32): keywords=SIP Trunk – Incoming call – 14xx      //
//      Originator phone type: 14xx                                 //
//      Destination phone type: 14xx                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase9:
{
    report(********** TestCase9 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncoming14XXCallSIP;
    gosub:Deconfiguration;
    report(********** TestCase9 COMPLETED **********):<null>;
}

//////////////////////////////////////////////////////////////////////
// Acceptance - TestCase10                                          //
//    SCENARIO (29): keywords=SIP Trunk – Outgoing call – POT       //
//    SCENARIO (23): keywords=SIP Trunk – Incoming call – POT       //
//      Originator phone type: POT                                  //
//      Destination phone type: ETR (call cannot be answered        //
//      correctly by POT)                                           //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase10:
{
    report(********** TestCase10 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncomingPOTCallSIP;
    gosub:Deconfiguration;
    report(********** TestCase10 COMPLETED **********):<null>;
}
////////////////////////////////////////////////////////////////////////////////
// Acceptance - TestCase11                                                    //
//    SCENARIO (30): keywords=SIP Trunk – Outgoing call – ETR/POT COMBO       //
//    SCENARIO (34): keywords=SIP Trunk – Incoming call – ETR/POT COMBO       //
//      Originator phone type: POT CONNECTED TO ETR CARD                      //
//      Destination phone type: ETR (call cannot be answered                  //
//      correctly by POT)                                                     //
//                                                                            //
////////////////////////////////////////////////////////////////////////////////
TestCase11:
{
    report(********** TestCase11 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncomingETRPOTCallSIP;
    gosub:Deconfiguration;
    report(********** TestCase11 COMPLETED **********):<null>;
}

/////////////////////////////////////////////////////////////////////
// Acceptance - TestCase12                                         //
//    SCENARIO (35): keywords=PRI Trunk – Outgoing call – ETR       //
//    SCENARIO (39): keywords=PRI Trunk – Incoming call – ETR       //
//      Originator phone type: ETR(34D)                            //
//      Destination phone type: ETR(18D)                           //
//                                                                 //
/////////////////////////////////////////////////////////////////////
TestCase12:
{
    report(********** TestCase12 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncomingETRCallT1;
    gosub:Deconfiguration;
    report(********** TestCase12 COMPLETED **********):<null>;
}

//////////////////////////////////////////////////////////////////////
// Acceptance - TestCase13                                          //
//    SCENARIO (36): keywords=T1 Trunk – Outgoing call – 14xx       //
//    SCENARIO (40): keywords=T1 Trunk – Incoming call – 14xx       //
//      Originator phone type: 14xx                                 //
//      Destination phone type: 14xx                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase13:
{
    report(********** TestCase13 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncoming14XXCallT1;
    gosub:Deconfiguration;
    report(********** TestCase13 COMPLETED **********):<null>;
}

//////////////////////////////////////////////////////////////////////
// Acceptance - TestCase14                                          //
//    SCENARIO (37): keywords=T1 Trunk – Outgoing call – POT        //
//    SCENARIO (41): keywords=T1 Trunk – Incoming call – POT        //
//      Originator phone type: POT                                  //
//      Destination phone type: ETR (call cannot be answered        //
//      correctly by POT)                                           //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase14:
{
    report(********** TestCase14 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncomingPOTCallT1;
    gosub:Deconfiguration;
    report(********** TestCase14 COMPLETED **********):<null>;
}
////////////////////////////////////////////////////////////////////////////////
// Acceptance - TestCase15                                                    //
//    SCENARIO (38): keywords=T1 Trunk – Outgoing call – ETR/POT COMBO        //
//    SCENARIO (42): keywords=T1 Trunk – Incoming call – ETR/POT COMBO        //
//      Originator phone type: POT CONNECTED TO ETR CARD                      //
//      Destination phone type: ETR (call cannot be answered                  //
//      correctly by POT)                                                     //
//                                                                            //
////////////////////////////////////////////////////////////////////////////////
TestCase15:
{
    report(********** TestCase15 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncomingETRPOTCallT1;
    gosub:Deconfiguration;
    report(********** TestCase15 COMPLETED **********):<null>;
}
////////////////////////////////////////////////////////////////////////////////
// Acceptance - TestCase16                                                    //
//    SCENARIO (46): keywords=Voicemail Leave                                 //
//                                                                            //
////////////////////////////////////////////////////////////////////////////////
TestCase16:
{
    report(********** TestCase16 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicLeaveVM;
    gosub:TestBasicDeleteVM;
    gosub:Deconfiguration;
    report(********** TestCase16 COMPLETED **********):<null>;
}
////////////////////////////////////////////////////////////////////////////////
// Acceptance - TestCase17                                                        //
//    SCENARIO (47): keywords=EVM Listen                                      //
//                                                                            //
////////////////////////////////////////////////////////////////////////////////
TestCase17:
{
    report(********** TestCase17 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicLeaveVM;
    gosub:TestBasicListenVM;
    gosub:TestBasicDeleteOldVM;
    gosub:Deconfiguration;
    report(********** TestCase17 COMPLETED **********):<null>;
}
////////////////////////////////////////////////////////////////////////////////
// Acceptance - TestCase18                                                        //
//    SCENARIO (48): keywords=EVM Delete                                      //
//                                                                            //
////////////////////////////////////////////////////////////////////////////////
TestCase18:
{
    report(********** TestCase18 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicLeaveVM;
    gosub:TestBasicDeleteVM;
    gosub:Deconfiguration;
    report(********** TestCase18 COMPLETED **********):<null>;
}
////////////////////////////////////////////////////////////////////////////////
// Acceptance - Test19                                                        //
//   SCENARIO (49): keywords=EVM Save                                         //
//                                                                            //
////////////////////////////////////////////////////////////////////////////////
TestCase19:
{
    report(********** TestCase19 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicLeaveVM;
    gosub:TestBasicListenVM;
    gosub:TestBasicSaveVM;
    gosub:TestBasicDeleteVM;
    gosub:Deconfiguration;
    report(********** TestCase19 COMPLETED **********):<null>;
}
////////////////////////////////////////////////////////////////////////////////
// Acceptance - TestCase20                                                    //
//    SCENARIO (51): keywords=Transfer – Assisted                             //
//                                                                            //
////////////////////////////////////////////////////////////////////////////////
TestCase20:
{
    report(********** TestCase20 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicAssistedTransfer;
    gosub:Deconfiguration;
    report(********** TestCase20 COMPLETED **********):<null>;
}

////////////////////////////////////////////////////////////////////////////////
// Acceptance - TestCase21                                                    //
//    SCENARIO (52): keywords=Transfer – Not Assisted                         //
//                                                                            //
////////////////////////////////////////////////////////////////////////////////
TestCase21:
{
    report(********** TestCase21 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicNotAssistedTransfer;
    gosub:Deconfiguration;
    report(********** TestCase21 COMPLETED **********):<null>;
}

/////////////////////////////////////////////////////////////////////////////////
// Acceptance - TestCase22                                                     //
//    SCENARIO (53): keywords=1400 Phone Display – Hold Call (1416/1408 Phones)//
//                                                                             //
/////////////////////////////////////////////////////////////////////////////////
TestCase22:
{
    report(********** TestCase22 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicHoldDisplay;
    gosub:Deconfiguration;
    report(********** TestCase22 COMPLETED **********):<null>;
}

////////////////////////////////////////////////////////////////////////////////
// Acceptance - TestCase23                                                    //
//    SCENARIO (54): keywords=Basic conference                                //
//                                                                            //
////////////////////////////////////////////////////////////////////////////////
TestCase23:
{
    report(********** TestCase23 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicConference;
    gosub:Deconfiguration;
    report(********** TestCase23 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - TestCase24                                          //
//    Added scenario: keywords=Analogue Trunk – Outgoing call – 14xx//
//    Added scenario: keywords=Analogue Trunk – Incoming call – 14xx//
//      Originator phone type: 14xx                                 //
//      Destination phone type: 14xx                                //
//    Purpose - test incoming call to extn57 (DS16)                 //
//////////////////////////////////////////////////////////////////////
TestCase24:
{
    report(********** TestCase24 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncoming14XXCallAnalog2;
    gosub:Deconfiguration;
    report(********** TestCase24 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - TestCase25                                          //
//    Added scenario: keywords=Analogue Trunk – Outgoing call – 14xx//
//    Added scenario: keywords=Analogue Trunk – Incoming call – 14xx//
//      Originator phone type: 14xx                                 //
//      Destination phone type: 14xx                                //
//    Purpose - test outgoing call from extn57 (DS16)               //
//////////////////////////////////////////////////////////////////////
TestCase25:
{
    report(********** TestCase25 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncoming14XXCallAnalog;
    gosub:Deconfiguration;
    report(********** TestCase25 COMPLETED **********):<null>;
}

//////////////////////////////////////////////////////////////////////
// Acceptance - TestCase26                                          //
//    SCENARIO (28): keywords=SIP Trunk – Outgoing call – 14xx      //
//    SCENARIO (32): keywords=SIP Trunk – Incoming call – 14xx      //
//      Originator phone type: 14xx                                 //
//      Destination phone type: 14xx                                //
//    Purpose - test incoming call to extn57 (DS16)                 //
//////////////////////////////////////////////////////////////////////
TestCase26:
{
    report(********** TestCase26 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncoming14XXCallSIP2;
    gosub:Deconfiguration;
    report(********** TestCase26 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - TestCase27                                          //
//    SCENARIO (28): keywords=SIP Trunk – Outgoing call – 14xx      //
//    SCENARIO (32): keywords=SIP Trunk – Incoming call – 14xx      //
//      Originator phone type: 14xx                                 //
//      Destination phone type: 14xx                                //
//    Purpose - test outgoing call from extn57 (DS16)
//////////////////////////////////////////////////////////////////////
TestCase27:
{
    report(********** TestCase27 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncoming14XXCallSIP;
    gosub:Deconfiguration;
    report(********** TestCase27 COMPLETED **********):<null>;
}

//////////////////////////////////////////////////////////////////////
// Acceptance - TestCase28                                          //
//    SCENARIO (36): keywords=T1 Trunk – Outgoing call – 14xx       //
//    SCENARIO (40): keywords=T1 Trunk – Incoming call – 14xx       //
//      Originator phone type: 14xx                                 //
//      Destination phone type: 14xx                                //
//     Purpose - test incoming call to extn57 (DS16)
//////////////////////////////////////////////////////////////////////
TestCase28:
{
    report(********** TestCase28 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncoming14XXCallT1_2;
    gosub:Deconfiguration;
    report(********** TestCase28 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - TestCase29                                          //
//    SCENARIO (36): keywords=T1 Trunk – Outgoing call – 14xx       //
//    SCENARIO (40): keywords=T1 Trunk – Incoming call – 14xx       //
//      Originator phone type: 14xx                                 //
//      Destination phone type: 14xx                                //
//     Purpose - test outgoing call from extn57 (DS16)
//////////////////////////////////////////////////////////////////////
TestCase29:
{
    report(********** TestCase29 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingIncoming14XXCallT1;
    gosub:Deconfiguration;
    report(********** TestCase29 COMPLETED **********):<null>;
}

/////////////////////////////////////////////////
// Acceptance - CALL SCRIPTS                   //
/////////////////////////////////////////////////

TestBasicFeature:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;

    // User A dials Feature 590 on idle screen
    report( - PressSoftKey <Feature> - ):<null>;
    set:User($UserA).cm_extn.DCP.MenuKey=B;
    wait:$wait_time;
    set:User($UserA).cm_extn.DCP.StdKey =5;
    set:User($UserA).cm_extn.DCP.StdKey =9;
    set:User($UserA).cm_extn.DCP.StdKey =0;
    wait:$delay_time;

    // Check Display for A
    set:Variable.Usr = $UserA;set:Variable.State = "F590";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;

    // User A exits
    report( - PressSoftKey <Exit> - ):<null>;
    set:User($UserA).cm_extn.DCP.MenuKey=C;
    wait:$delay_time;

    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;

    // User A dials Feature 591 on idle screen
    report( - PressSoftKey <Feature> - ):<null>;
    set:User($UserA).cm_extn.DCP.MenuKey=B;
    wait:$wait_time;
    set:User($UserA).cm_extn.DCP.StdKey =5;
    set:User($UserA).cm_extn.DCP.StdKey =9;
    set:User($UserA).cm_extn.DCP.StdKey =1;
    wait:$delay_time;

    // Check Display for A
    set:Variable.Usr = $UserA;set:Variable.State = "F591";set:Variable.PType = "1516";set:Variable.OtherExtn=$PartnerIP;
    gosub:CheckDisplay;

    // User A exits
    report( - PressSoftKey <Exit> - ):<null>;
    set:User($UserA).cm_extn.DCP.MenuKey=C;
    wait:$delay_time;

    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
}

TestBasicUpgrade:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User C IDLE
    set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallC_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B offhook
        set:User($UserB).cm_extn.DCP.HookChange = OffHook;
        set:User($UserB).cm_extn.DCP.DSS[$OutgoingCall_dssKey] = Press;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;

        // B dials external number
        set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;
    }
    if($RunMode == Simulator):
    {
        gosub:MakeICAlogTrunkCall;
    }

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserC).cm_extn.current_ep.state=CMCSRinging;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;
    }

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "EXT_RINGBACK";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User C Ringing
    set:Variable.Usr = $UserC;set:Variable.State = "EXT_RING";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallC_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;
    }

    // Talkpath between A & B
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    }
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CALLED_CONN";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User C Idle
    set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PhoneType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallC_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
    if($RunMode == Rig):
    {
        set:User($UserB).cm_extn.OnHook;
    }

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
    }
    sync($sync_delay_time):User($UserC).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B Idle
        set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User C Idle
    set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PhoneType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallC_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}


TestBasicEmbeddedVM:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User C IDLE
    set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallC_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A offhook
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;
    set:User($UserA).cm_extn.DCP.DSS[$VMCallA_dssKey] = Press;
    wait:$delay_time;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSDialling;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneDial;
    verify(Tone Verification Issue: $UserA is not in dialing state):User($UserA).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // User A DIAL
    set:Variable.Usr = $UserA;set:Variable.State = "DIAL";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A dials 777
    set:User($UserA).cm_extn.DialWithGaps.1000=777;
    wait:$delay_time;

    // User A connected to VM
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state = CMCSConnected;
    verify(Tone Verification Issue: $UserA is not in connected state):User($UserA).cm_extn.current_ep.state = CMCSConnected;
    //commented this because VMail object cannot be used properly
    //sync($sync_delay_time):VMail($ExtnA).state = CMCSConnected;
    //verify(VMail call is not connected):VMail($ExtnA).state = CMCSConnected;

    // Check display for A connected to VM
    set:Variable.Usr = $UserA;set:Variable.State = "VM_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    wait:$wait_time;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    set:User($UserB).cm_extn.DCP.DSS[$VMCallB_dssKey] = Press;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneDial;
    wait:$delay_time;

    // User B DIAL
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B dials 777
    set:User($UserB).cm_extn.DialWithGaps.1000=777;
    wait:$delay_time;

    // User B connected to VM
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state = CMCSConnected;
    //commented this because VMail object cannot be used properly
    //sync($sync_delay_time):VMail($ExtnB).state = CMCSConnected;
    //verify(VMail call is not connected):VMail($ExtnB).state = CMCSConnected;

    // Check display for B connected to VM
    set:Variable.Usr = $UserB;set:Variable.State = "VM_CONN";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    wait:$wait_time;

    // User C offhook
    set:User($UserC).cm_extn.DCP.HookChange = OffHook;
    set:User($UserC).cm_extn.DCP.DSS[$VMCallC_dssKey] = Press;
    sync($sync_delay_time):User($UserC).cm_extn.current_ep.state=CMCSDialling;
    sync($sync_delay_time):User($UserC).cm_extn.current_ep.GetActiveTone=CMLocalToneDial;
    verify(Tone Verification Issue: $UserC is not in dialing state):User($UserC).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // User C DIAL
    set:Variable.Usr = $UserC;set:Variable.State = "DIAL";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallC_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User C dials 777
    set:User($UserC).cm_extn.DialWithGaps.1000=777;
    wait:$delay_time;

    // User C gets ringback tone from VM
    sync($sync_delay_time):User($UserC).cm_extn.current_ep.state = CMCSRingBack;
    verify(Tone Verification Issue: $UserC is not in ringback state):User($UserC).cm_extn.current_ep.state = CMCSRingBack;

    // Check display for C in ringback state
    set:Variable.Usr = $UserC;set:Variable.State = "RINGBACK";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallC_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    wait:$delay_time;

    // User B goes onhook and eliberates one VM channel
    set:User($UserB).cm_extn.DCP.HookChange = OnHook;
    wait:$delay_time;
    wait:$delay_time;

    // User A & C are conected to VM
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    //sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSIdle;
    sync($sync_delay_time):User($UserC).cm_extn.current_ep.state=CMCSConnected;
    //verify(Tone Verification Issue: $UserB is not in idle state):User($UserB).cm_extn.current_ep.state=CMCSIdle;

    // User A CONNECTED
    set:Variable.Usr = $UserA;set:Variable.State = "VM_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User C CONNECTED
    set:Variable.Usr = $UserC;set:Variable.State = "VM_CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallC_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A & C hang up
    set:User($UserA).cm_extn.DCP.HookChange = OnHook;
    set:User($UserC).cm_extn.DCP.HookChange = OnHook;
    wait:$delay_time;

    // User A, User B and User C idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserC).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User C Idle
    set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PhoneType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallC_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicOutgoingIncomingETRCallAnalog:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B offhook
        set:User($UserB).cm_extn.DCP.HookChange = OffHook;
        set:User($UserB).cm_extn.DCP.DSS[$OutgoingCallB_dssKey] = Press;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;

        // B dials external number
        set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;
    }
    if($RunMode == Simulator):
    {
        gosub:MakeICAlogTrunkCall;
    }

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;
    }

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected/ringback
        set:Variable.Usr = $UserB;set:Variable.State = "EXT_RINGBACK_CALL";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;
    }

    // Talkpath between A & B
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    }
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CALLED_CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
    if($RunMode == Rig):
    {
        set:User($UserB).cm_extn.OnHook;
    }

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
    }

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B Idle
        set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }
}

TestBasicOutgoingIncomingETRCallSIP:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    set:User($UserB).cm_extn.DCP.DSS[$OutgoingCallB_dssKey] = Press;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$wait_time;

    // Check DIAL display and lamps for B
    wait:$delay_time;
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING_SIP";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected/ringback
    set:Variable.Usr = $UserB;set:Variable.State = "EXT_RINGBACK_CALL";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
      set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom2B_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicOutgoingIncomingETRCallT1:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    set:User($UserB).cm_extn.DCP.DSS[$OutgoingCallB_dssKey] = Press;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$wait_time;

    // Check DIAL display and lamps for B
    wait:$delay_time;
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING_EXTERNAL";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected/ringback
    set:Variable.Usr = $UserB;set:Variable.State = "EXT_RINGBACK_CALL";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CONN_EXTERNAL";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
      set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicOutgoingIncoming14XXCallAnalog:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B IDLE
        set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
        gosub:CheckLamps;

        // User B offhook
        set:User($UserB).cm_extn.DCP.DSS[$OutgoingCallB_dssKey] = Press;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;

        // B dials external number
        set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;
    }
    if($RunMode == Simulator):
    {
        gosub:MakeICAlogTrunkCall;
    }

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;
    }

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "EXT_RINGBACK";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;
    }

    // Talkpath between A & B
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    }
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CALLED_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
    if($RunMode == Rig):
    {
        set:User($UserB).cm_extn.OnHook;
    }

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
    }

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B Idle
        set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }
}
TestBasicOutgoingIncoming14XXCallAnalog2:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B IDLE
        set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
        gosub:CheckLamps;

        // User B offhook
        set:User($UserB).cm_extn.DCP.DSS[$OutgoingCallB_dssKey] = Press;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;

        // B dials external number
        set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;
    }
    if($RunMode == Simulator):
    {
        gosub:MakeICAlogTrunkCall;
    }

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;
    }

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "EXT_RINGBACK";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;
    }

    // Talkpath between A & B
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    }
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CALLED_CONN";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
    if($RunMode == Rig):
    {
        set:User($UserB).cm_extn.OnHook;
    }

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
    }

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B Idle
        set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }
}

TestBasicOutgoingIncoming14XXCallSIP:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.DSS[$OutgoingCallB_dssKey] = Press;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "EXT_CALLED_CALL";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$ExtnB;

    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CONN";set:Variable.PType = "1508";set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
    set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicOutgoingIncoming14XXCallSIP2:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.DSS[$OutgoingCallB_dssKey] = Press;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING_SIP";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "EXT_CALLED_CALL";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "CONN";set:Variable.PType = "1508";set:Variable.OtherExtn=$ExtnB;

    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
    set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}


TestBasicOutgoingIncoming14XXCallT1:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B offhook
    //set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    set:User($UserB).cm_extn.DCP.DSS[$OutgoingCallB_dssKey] = Press;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    verify(Tone Verification Issue: $UserB is not in dialing state):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING_EXTERNAL";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "EXT_RINGBACK_CALL";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CONN_EXTERNAL";set:Variable.PType = "1516";set:Variable.OtherExtn="";

    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
      set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicOutgoingIncoming14XXCallT1_2:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B offhook
    //set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    set:User($UserB).cm_extn.DCP.DSS[$OutgoingCallB_dssKey] = Press;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING_EXTERNAL";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "EXT_RINGBACK_CALL";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CONN_EXTERNAL";set:Variable.PType = "1508";set:Variable.OtherExtn="";

    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
      set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicOutgoingIncomingPOTCallAnalog:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B - IDLE (POT) - nothing to check

        // User B offhook
        set:User($UserB).cm_extn.FlashHook = True;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;

        // B dials external number
        set:User($UserB).cm_extn.DialWithGaps.100=$IPOExtn1;
    }
    if($RunMode == Simulator):
    {
        gosub:MakeICAlogTrunkCall;
    }

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSOGConnReq;
    }

    // User A Ringing
    //set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected - not verified (pots)

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSOGConnReq;
    }

    // Talkpath between A & B
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    }
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CALLED_CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected - not verified (pots)

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
    if($RunMode == Rig):
    {
         set:User($UserB).cm_extn.OnHook;
    }

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
    }

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicOutgoingIncomingETRPOTCallAnalog:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B - IDLE (POT) - nothing to check

    if($RunMode == Rig):
    {
        // User B offhook
        set:User($UserB).cm_extn.FlashHook = True;
        //sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
        //verify(Tone Verification Issue: $UserB is not in dialing state):User($UserB).cm_extn.current_ep.state=CMCSDialling;
        wait:$delay_time;

        // B dials external number
        set:User($UserB).cm_extn.DialWithGaps.200=$IPOExtn1;
    }
    if($RunMode == Simulator):
    {
        gosub:MakeICAlogTrunkCall;
    }

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;
    }

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
//    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected - not verified (pots)

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;
    }

    // Talkpath between A & B
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    }
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CALLED_CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected - not verified (pots)

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
    if($RunMode == Rig):
    {
        set:User($UserB).cm_extn.OnHook;
    }

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
    }

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicOutgoingIncomingPOTCallSIP:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B - IDLE (POT) - nothing to check

    // User B offhook
    set:User($UserB).cm_extn.FlashHook = True;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.500=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING_SIP";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected - not verified (pots)

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSOGConnReq;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected - not verified (pots)

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
      set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicOutgoingIncomingETRPOTCallSIP:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B - IDLE (POT) - nothing to check

    // User B offhook
    set:User($UserB).cm_extn.FlashHook = True;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.500=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING_SIP";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected - not verified (pots)

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected - not verified (pots)

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
      set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicOutgoingIncomingPOTCallT1:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B - IDLE (POT) - nothing to check

    // User B offhook
    set:User($UserB).cm_extn.FlashHook = True;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.500=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING_EXTERNAL";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected - not verified (pots)

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSOGConnReq;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CONN_EXTERNAL";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected - not verified (pots)

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
      set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicOutgoingIncomingETRPOTCallT1:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B - IDLE (POT) - nothing to check

    // User B offhook
    set:User($UserB).cm_extn.FlashHook = True;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.500=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING_EXTERNAL";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected - not verified (pots)

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCallA_dssKey] = Press;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CONN_EXTERNAL";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected - not verified (pots)

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
      set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicLeaveVM:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom2B_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A offhook
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;
    set:User($UserA).cm_extn.DCP.DSS[$Icom1A_dssKey] = Press;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSDialling;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneDial;
    wait:$delay_time;

    // User A DIAL
    set:Variable.Usr = $UserA;set:Variable.State = "DIAL";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A dials B
    set:User($UserA).cm_extn.DialWithGaps.1000=$ExtnB;
    wait:$ring_time;

    // User B ringing
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRingBack;

    // User A RINGBACK
    set:Variable.Usr = $UserA;set:Variable.State = "RINGBACK";set:Variable.PType = "1516";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B RING
    set:Variable.Usr = $UserB;set:Variable.State = "RING";set:Variable.PType = "1508";set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom2B_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B press drop button to divert the call to VM
    set:User($UserB).cm_extn.DCP.FeatureKey = DCPLFeatureDrop;
    wait:$delay_time;

    // User A connected to VM
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state = CMCSConnected;
    //commented this because VMail object cannot be used properly
    // issue: Subsystem(VMail) Element() Found(VoiceMail is not VoicemailLine/VoicemailPC) Expected((null))
    //sync($sync_delay_time):VMail($ExtnA).state = CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // Check display for A connected to VM
    set:Variable.Usr = $UserA;set:Variable.State = "VM_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    wait:$wait_time;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom2B_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // Wait for VM prompt to start entering the new message
    wait:$connect_time;

    // Start entering the new message
    set:Variable.digit=0;
    while($digit<=9):
    {
        set:User($UserA).cm_extn.DCP.StdKey =$digit;
        wait:$wait_time;
        set:Variable.digit = $digit + 1;
    }
    set:User($UserA).cm_extn.DCP.StdKey =#;
    wait:$wait_time;
    set:User($UserA).cm_extn.OnHook;
    wait:$delay_time;

    // commented because we cannot process at this time - this type of verification
    //sync($sync_delay_time):User($UserB).cm_extn.message_waiting_lamp = On;
    //verify(MWI is Unlit):User($UserB).cm_extn.message_waiting_lamp = On;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1A_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom2B_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicListenVM:
{
    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    set:User($UserB).cm_extn.DCP.DSS[$Icom1B_dssKey] = Press;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneDial;
    wait:$delay_time;

    // User B DIAL
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B dials 777
    set:User($UserB).cm_extn.DialWithGaps.1000=777;
    wait:$connected_time;

    // User  B connected to VM
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state = CMCSConnected;

    // Check display for B connected to VM
    set:Variable.Usr = $UserB;set:Variable.State = "VM_CONN";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    wait:$wait_time;

    // Listen to the new message
    wait:$VM_connect_time;

    // User B
    set:User($UserB).cm_extn.OnHook;
    wait:$delay_time;

    // commented because we cannot process at this time - this type of verification
    //sync($sync_delay_time):User($UserB).cm_extn.message_waiting_lamp = Off;

    // User B idle
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
    verify(Tone Verification Issue: $UserB is not idle):User($UserB).cm_extn.state=CMCSIdle;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicDeleteVM:
{
    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    set:User($UserB).cm_extn.DCP.DSS[$Icom1B_dssKey] = Press;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneDial;
    wait:$delay_time;

    // User B DIAL
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B dials 777
    set:User($UserB).cm_extn.DialWithGaps.1000=777;
    wait:$delay_time;

    // User  B connected to VM
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state = CMCSConnected;

    // Check display for B connected to VM
    set:Variable.Usr = $UserB;set:Variable.State = "VM_CONN";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    wait:$delay_time;
    wait:$delay_time;

    // Delete the new message
    set:User($UserB).cm_extn.DCP.StdKey =4;
    wait:$delay_time;
    set:User($UserB).cm_extn.DCP.StdKey =4;
    wait:$delay_time;

    // User B
    set:User($UserB).cm_extn.OnHook;
    wait:$delay_time;

    // commented because we cannot process at this time - this type of verification
    //sync($sync_delay_time):User($UserB).cm_extn.message_waiting_lamp = Off;

    // User B idle
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicDeleteOldVM:
{
    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    set:User($UserB).cm_extn.DCP.DSS[$Icom1B_dssKey] = Press;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneDial;
    wait:$delay_time;

    // User B DIAL
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B dials 777
    set:User($UserB).cm_extn.DialWithGaps.1000=777;
    wait:$delay_time;
    wait:$delay_time;

    // User  B connected to VM
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state = CMCSConnected;
    verify(Tone Verification Issue: $UserB is not in connected state):User($UserB).cm_extn.current_ep.state = CMCSConnected;

    // Check display for B connected to VM
    set:Variable.Usr = $UserB;set:Variable.State = "VM_CONN";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    wait:$wait_time;

    // Go to old messages
    set:User($UserB).cm_extn.DCP.StdKey =1;
    wait:$delay_time;
    wait:$delay_time;

    // Delete old message
    set:User($UserB).cm_extn.DCP.StdKey =4;
    wait:$delay_time;

    // User B
    set:User($UserB).cm_extn.OnHook;
    wait:$delay_time;

    // commented because we cannot process at this time - this type of verification
    //sync($sync_delay_time):User($UserB).cm_extn.message_waiting_lamp = Off;

    // User B idle
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicSaveVM:
{
    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    set:User($UserB).cm_extn.DCP.DSS[$Icom1B_dssKey] = Press;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneDial;
    wait:$delay_time;

    // User B DIAL
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B dials 777
    set:User($UserB).cm_extn.DialWithGaps.1000=777;
    wait:$connect_time;

    // User  B connected to VM
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state = CMCSConnected;

    // Check display for B connected to VM
    set:Variable.Usr = $UserB;set:Variable.State = "VM_CONN";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    wait:$wait_time;

    // Save message
    set:User($UserB).cm_extn.DCP.StdKey =5;
    wait:$delay_time;

    // User B
    set:User($UserB).cm_extn.OnHook;
    wait:$delay_time;

    // commented because we cannot process at this time - this type of verification
    //sync($sync_delay_time):User($UserB).cm_extn.message_waiting_lamp = On;

    // User B idle
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $Icom1B_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}


TestBasicAssistedTransfer:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C IDLE
        set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
        gosub:CheckLamps;

        // User C offhook
        set:User($UserC).cm_extn.DCP.DSS[$OutgoingCall_dssKey] = Press;
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.state=CMCSDialling;

        // C dials external number
        set:User($UserC).cm_extn.DialWithGaps.1000=$IPOExtn1;
    }
    if($RunMode == Simulator):
    {
        gosub:MakeICAlogTrunkCall;
    }
    wait:$ring_time;

    // User A ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.state=CMCSConnected;
    }

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C connected
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_RINGBACK";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCall_dssKey] = Press;

    wait:$connect_time;

    // User A and User C connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.state=CMCSConnected;
    }

    // Talkpath between A & C
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    }
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CALLED_CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C connected
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }
    // A Initiate asissted transfer
    set:User($UserA).cm_extn.DCP.FeatureKey = DCPLFeatureXfer;
    sync(5000):User($UserA).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // User A dial
    set:Variable.Usr = $UserA;set:Variable.State = "DIAL";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Wink";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Wink";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C connected
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // A dials B
    set:User($UserA).cm_extn.DialWithGaps.2000=$ExtnB;
    wait:$transfer_ring_time;

    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRingBack;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRinging;

    // User A dial
    set:Variable.Usr = $UserA;set:Variable.State = "RING";set:Variable.PType = "ETR";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Wink";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B called
    set:Variable.Usr = $UserB;set:Variable.State = "ENQUIRE_RING";set:Variable.PType = "ETR";set:Variable.OExt1=$IPOExtn2;
    set:Variable.OExt2=$ExtnA;
    gosub:CheckDisplay;
    //set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Wink";
    //gosub:CheckLamps;
    if($RunMode == Rig):
    {
        set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    }
    if($RunMode == Simulator):
    {
        set:Variable.Btn = $Icom2_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    }
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C connected to trunk
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User B answers the enquiry call
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    wait:$transfer_ring_time;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A CONN
    set:Variable.Usr = $UserA;set:Variable.State = "CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Wink";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B CONN
    set:Variable.Usr = $UserB;set:Variable.State = "CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Wink";
    gosub:CheckLamps;
    if($RunMode == Rig):
    {
        set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    }
    if($RunMode == Simulator):
    {
        set:Variable.Btn = $Icom2_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    }
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C connected to trunk
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User A completes transfer
    set:User($UserA).cm_extn.DCP.FeatureKey = DCPLFeatureXfer;
    sync($sync_delay_time):User($UserA).cm_extn.state=CMESPortRecoverDelay;
    wait:$transfer_ring_time;

    // Talkpath between C & B
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    }
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B CONN
    set:Variable.Usr = $UserB;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    if($RunMode == Rig):
    {
        set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    }
    if($RunMode == Simulator):
    {
        set:Variable.Btn = $Icom2_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    }
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C CONN
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // C & B onhook
    if($RunMode == Rig):
    {
      set:User($UserC).cm_extn.OnHook;
    }
    set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A , B and C idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.state=CMCSIdle;
    }

   // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C IDLE
        set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }
}

TestBasicNotAssistedTransfer:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C IDLE
        set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
        gosub:CheckLamps;

        // User C offhook
        set:User($UserC).cm_extn.DCP.DSS[$OutgoingCall_dssKey] = Press;
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.state=CMCSDialling;

        // C dials external number
        set:User($UserC).cm_extn.DialWithGaps.1000=$IPOExtn1;
        wait:$ring_time;
    }
    if($RunMode == Simulator):
    {
        gosub:MakeICAlogTrunkCall;
    }

    // User A ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.state=CMCSConnected;
    }

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C connected
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_RINGBACK";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCall_dssKey] = Press;

    wait:$connect_time;

    // User A and User C connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.state=CMCSConnected;
    }

    // Talkpath between A & C
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    }
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CALLED_CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C connected
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // A Initiate asissted transfer
    set:User($UserA).cm_extn.DCP.FeatureKey = DCPLFeatureXfer;
    sync(5000):User($UserA).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // User A dial
    set:Variable.Usr = $UserA;set:Variable.State = "DIAL";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Wink";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Wink";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C connected
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // A dials B
    set:User($UserA).cm_extn.DialWithGaps.2000=$ExtnB;
    wait:$transfer_ring_time;

    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRingBack;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRinging;

    // User A dial
    set:Variable.Usr = $UserA;set:Variable.State = "RING";set:Variable.PType = "ETR";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Wink";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B called
    set:Variable.Usr = $UserB;set:Variable.State = "ENQUIRE_RING";set:Variable.PType = "ETR";set:Variable.OExt1=$IPOExtn2;
    set:Variable.OExt2=$ExtnA;
    gosub:CheckDisplay;
    //set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Wink";
    //gosub:CheckLamps;
    if($RunMode == Rig):
    {
        set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    }
    if($RunMode == Simulator):
    {
        set:Variable.Btn = $Icom2_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    }
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C connected to trunk
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User A completes transfer
    set:User($UserA).cm_extn.DCP.FeatureKey = DCPLFeatureXfer;
    sync($sync_delay_time):User($UserA).cm_extn.state=CMESPortRecoverDelay;
    wait:$transfer_ring_time;

    // Talkpath between C & B
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRinging;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.state=CMCSConnected;
    }

    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B CALLED
    set:Variable.Usr = $UserB;set:Variable.State = "ENQUIRE_RING";set:Variable.PType = "ETR";set:Variable.OExt1=$IPOExtn2;
    set:Variable.OExt2=$ExtnA;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C CONN
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User B answers the enquiry call
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    wait:$transfer_ring_time;

    // Talkpath between C & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    }

    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B CONN
    set:Variable.Usr = $UserB;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C CONN
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // C & B onhook
    if($RunMode == Rig):
    {
        set:User($UserC).cm_extn.OnHook;
    }
    set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A , B and C idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.state=CMCSIdle;
    }

   // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B CONN
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C CONN
        set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }
}

TestBasicHoldDisplay:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A offhook
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;
    set:User($UserA).cm_extn.DCP.DSS[$OutgoingCall_dssKey] = Press;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSDialling;
    verify(Tone Verification Issue: $UserA is not in dialing state):User($UserA).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // User A DIAL
    set:Variable.Usr = $UserA;set:Variable.State = "DIAL";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // A dials B
    set:User($UserA).cm_extn.DialWithGaps.1000=$ExtnB;
    wait:$ring_time;

    // User B ringing
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRingBack;

    // User A RINGBACK
    set:Variable.Usr = $UserA;set:Variable.State = "RINGBACK";set:Variable.PType = "1516";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B RING
    set:Variable.Usr = $UserB;set:Variable.State = "RING";set:Variable.PType = "1508";set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B Answers
    set:User($UserB).cm_extn.DCP.DSS[$IncomingCall_dssKey] = Press;
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
    set:Variable.Usr = $UserA;set:Variable.State = "CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B CONN
    set:Variable.Usr = $UserB;set:Variable.State = "CONN";set:Variable.PType = "1508";set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B puts user A on hold
    set:User($UserB).cm_extn.DCP.FeatureKey = DCPLFeatureHold;
    wait:$hold_time;

    // User A is HELD
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneHoldMusic;
    verify(Tone Verification Issue: $UserA is not held):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneHoldMusic;

    // User A HELD
    set:Variable.Usr = $UserA;set:Variable.State = "HELD";set:Variable.PType = "1516";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Wink";
    gosub:CheckLamps;

    // User B HOLD
    set:Variable.Usr = $UserB;set:Variable.State = "HOLD";set:Variable.PType = "1508";set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Wink";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B Retrieves the call
    set:User($UserB).cm_extn.DCP.MenuKey=C;
    set:User($UserB).cm_extn.DCP.MenuKey=A;
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
    set:Variable.Usr = $UserA;set:Variable.State = "CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B CONN
    set:Variable.Usr = $UserB;set:Variable.State = "CONN";set:Variable.PType = "1508";set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User A puts user B on hold
    set:User($UserA).cm_extn.DCP.FeatureKey = DCPLFeatureHold;
    wait:$hold_time;

    // UserB is held
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneHoldMusic;
    verify(Tone Verification Issue: $UserB is not held):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneHoldMusic;

    // User A HOLD
    set:Variable.Usr = $UserA;set:Variable.State = "HOLD";set:Variable.PType = "1516";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="Wink";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B HELD
    set:Variable.Usr = $UserB;set:Variable.State = "HELD";set:Variable.PType = "1508";set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Wink";
    gosub:CheckLamps;

    // User A Retrieves the call
    set:User($UserA).cm_extn.DCP.MenuKey=A;
    wait:$hold_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSConnected;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // A & B onhook
    set:User($UserA).cm_extn.OnHook;
      set:User($UserB).cm_extn.OnHook;
    wait:$hold_time;

    // User A , B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
}

TestBasicConference:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C IDLE
        set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
        gosub:CheckLamps;

        // User C offhook
        set:User($UserC).cm_extn.DCP.DSS[$OutgoingCall_dssKey] = Press;
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.state=CMCSDialling;

        // C dials external number
        set:User($UserC).cm_extn.DialWithGaps.1000=$IPOExtn1;
    }
    if($RunMode == Simulator):
    {
        gosub:MakeICAlogTrunkCall;
    }

    wait:$ring_time;

    // User A ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.state=CMCSConnected;
    }

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_RING";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C connected
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_RINGBACK";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User A Answers
    set:User($UserA).cm_extn.DCP.DSS[$IncomingCall_dssKey] = Press;

    wait:$connect_time;

    // User A and User C connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.state=CMCSConnected;
    }

    // Talkpath between A & C
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    }
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CALLED_CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C connected
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // A Initiate conference
    set:User($UserA).cm_extn.DCP.FeatureKey = DCPLFeatureConf;
    sync(5000):User($UserA).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // User A dial
    set:Variable.Usr = $UserA;set:Variable.State = "DIAL";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Wink";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Wink";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C connected
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // A dials B
    set:User($UserA).cm_extn.DialWithGaps.2000=$ExtnB;
    wait:$transfer_ring_time;

    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRingBack;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRinging;

    // User A RING
    set:Variable.Usr = $UserA;set:Variable.State = "RING";set:Variable.PType = "ETR";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Wink";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B called
    set:Variable.Usr = $UserB;set:Variable.State = "RINGBACK";set:Variable.PType = "ETR";set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    //set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Wink";
    //gosub:CheckLamps;
    if($RunMode == Rig):
    {
        set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    }
    if($RunMode == Simulator):
    {
        set:Variable.Btn = $Icom2_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Off";
    }
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C connected to trunk
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User B answers the enquiry call
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    wait:$transfer_ring_time;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A CONN
    set:Variable.Usr = $UserA;set:Variable.State = "CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$ExtnB;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Wink";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B CONN
    set:Variable.Usr = $UserB;set:Variable.State = "CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn=$ExtnA;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Wink";
    gosub:CheckLamps;
    if($RunMode == Rig):
    {
        set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    }
    if($RunMode == Simulator):
    {
        set:Variable.Btn = $Icom2_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
    }
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C connected to trunk
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // User A completes conference
    set:User($UserA).cm_extn.DCP.FeatureKey = DCPLFeatureConf;
    wait:$transfer_ring_time;

    // Talkpath between C & B
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
        sync($sync_delay_time):User($UserC).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    }
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A CONF
    set:Variable.Usr = $UserA;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Flash";
    gosub:CheckLamps;

    // User B CONF
    set:Variable.Usr = $UserB;set:Variable.State = "CONF";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
    if($RunMode == Rig):
    {
        set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Flash";
    }
    if($RunMode == Simulator):
    {
        set:Variable.Btn = $Icom2_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="Flash";
    }
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C CONN
        set:Variable.Usr = $UserC;set:Variable.State = "EXT_CALLER_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }

    // A, C & B onhook
    set:User($UserA).cm_extn.OnHook;
    if($RunMode == Rig):
    {
       set:User($UserC).cm_extn.OnHook;
      }
    set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A , B and C idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserC).cm_extn.state=CMCSIdle;
    }

   // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "ETR";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;
    set:Variable.Btn = $Icom1_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User C CONN
        set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="Off";
        gosub:CheckLamps;
    }
}
/////////////////////////////////////////////////////////////////////////////

Configuration:
{
    report(*** Started doing phone configuration for test no: $TestID ***):<null>;

    if( $TestID == 1 ):
    {
        set:Variable.UserA = $x20_UserName;
        set:Variable.PhTyA = $x20_PhoneType;
        set:Variable.UserB = $x19_UserName;
        set:Variable.PhTyB = $x19_PhoneType;
        set:Variable.UserC = $x10_UserName;
        set:Variable.PhTyC = $x10_PhoneType;
        set:Variable.IncomingCallA_dssKey=6;   //1508: LA01 - Analog Trunk
        set:Variable.IncomingCallC_dssKey=2;   // ETR: LA01 - Analog Trunk
        set:Variable.OutgoingCall_dssKey=12;   //1516: LA02 - Analog Trunk
        set:Variable.IPOExtn1 = 209; // IPOffice called number
        set:Variable.IPOExtn2 = 210; //IPOffice callback number
        set:Variable.TrunkID = 5; // Analog Trunk used to make incoming calls
    }
    if( $TestID == 2 ):
    {
        set:Variable.UserA = $x19_UserName;
        set:Variable.UserB = $x20_UserName;
        set:Variable.UserC = $x10_UserName;
        set:Variable.VMCallA_dssKey = 15;
        set:Variable.VMCallB_dssKey = 4;
        set:Variable.VMCallC_dssKey = 0;
    }
    if( $TestID == 3 ):
    {
        set:Variable.UserA = $x19_UserName;
        set:Variable.PhTyA = $x19_PhoneType;
        set:Variable.PartnerIP = 192.168.42.120;
    }
    if( $TestID == 4 ):
    {
        set:Variable.UserA = $x10_UserName;
        set:Variable.UserB = $x11_UserName;
        set:Variable.IncomingCallA_dssKey=2;   //UserA:LA01 - ANALOG TRUNK
        set:Variable.OutgoingCallB_dssKey=3;   //UserB:LA02 - ANALOG TRUNK
        set:Variable.IPOExtn1 = 209;           //IPOffice number
        set:Variable.IPOExtn2 = 210;
        set:Variable.TrunkID = 5; // Analog Trunk used to make incoming calls
    }
    if( $TestID == 5 ):
    {
        set:Variable.UserA = $x19_UserName;
        set:Variable.UserB = $x20_UserName;
        set:Variable.IncomingCallA_dssKey=13;   //UserA:LA01 - ANALOG TRUNK
        set:Variable.OutgoingCallB_dssKey=7;    //UserB:LA02 - ANALOG TRUNK
        set:Variable.IPOExtn1 = 209;            //IPOffice number
        set:Variable.IPOExtn2 = 210;
        set:Variable.TrunkID = 5; // Analog Trunk used to make incoming calls
    }
    if( $TestID == 6 ):
    {
        set:Variable.UserA = $x10_UserName;
        set:Variable.UserB = $x24_UserName;
        set:Variable.IncomingCallA_dssKey=2;  //UserA:LA01 - ANALOG TRUNK
        set:Variable.OutgoingCallB_dssKey=0;  //UserB:POT
        set:Variable.IPOExtn1 = 802209;         //IPOffice number
        set:Variable.IPOExtn2 = 210;
        set:Variable.TrunkID = 5; // Analog Trunk used to make incoming calls
    }
    if( $TestID == 7 ):
    {
        set:Variable.UserA = $x10_UserName;
        set:Variable.UserB = $x14_UserName;
        set:Variable.IncomingCallA_dssKey=2;  //UserA:LA01 - ANALOG TRUNK
        set:Variable.OutgoingCallB_dssKey=0;  //UserB:POT
        set:Variable.IPOExtn1 = 802209;         //IPOffice number
        set:Variable.IPOExtn2 = 210;            //IPOffice number
        set:Variable.TrunkID = 5; // Analog Trunk used to make incoming calls
    }
    // SIP
    if( $TestID == 8 ):
    {
        set:Variable.UserA = $x10_UserName;
        set:Variable.UserB = $x11_UserName;
        set:Variable.ExtnA = $x10_UserNum;
        set:Variable.ExtnB = $x11_UserNum;
        set:Variable.Icom1A_dssKey=0;   //UserA:LA01 - SIP TRUNK
        set:Variable.Icom1B_dssKey=0;    //UserB:LA02 - SIP TRUNK
        set:Variable.IncomingCallA_dssKey=6;   //UserA:LA01 - SIP TRUNK
        set:Variable.OutgoingCallB_dssKey=7;   //UserB:LA02 - SIP TRUNK
        set:Variable.IPOExtn1 = 201;           //IPOffice number
    }
    if( $TestID == 9 ):
    {
        set:Variable.UserA = $x19_UserName;
        set:Variable.UserB = $x20_UserName;
        set:Variable.ExtnA = $x19_UserNum;
        set:Variable.ExtnB = $x20_UserNum;
        set:Variable.IncomingCallA_dssKey=8;   //UserA:LA01 - SIP TRUNK
        set:Variable.OutgoingCallB_dssKey=2;    //UserB:LA02 - SIP TRUNK
        set:Variable.Icom1A_dssKey=15;   //UserA:LA01 - SIP TRUNK
        set:Variable.Icom1B_dssKey=4;    //UserB:LA02 - SIP TRUNK
        set:Variable.IPOExtn1 = 201;            //IPOffice number
    }
    if( $TestID == 10 ):
    {
        set:Variable.UserA = $x10_UserName;
        set:Variable.UserB = $x24_UserName;
        set:Variable.ExtnA = $x10_UserNum;
        set:Variable.ExtnB = $x24_UserNum;
        set:Variable.Icom1A_dssKey=0;   //UserA:LA01 - SIP TRUNK
        set:Variable.IncomingCallA_dssKey=6;  //UserA:LA01 - ANALOG TRUNK
        set:Variable.OutgoingCallB_dssKey=0;  //UserB:POT
        set:Variable.IPOExtn1 = 814201;         //IPOffice number
        set:Variable.IPOExtn2 = 201;         //IPOffice number
    }
    if( $TestID == 11 ):
    {
        set:Variable.UserA = $x10_UserName;
        set:Variable.UserB = $x14_UserName;
        set:Variable.ExtnA = $x10_UserNum;
        set:Variable.ExtnB = $x14_UserNum;
        set:Variable.IncomingCallA_dssKey=6;  //UserA:LA01 - ANALOG TRUNK
        set:Variable.OutgoingCallB_dssKey=0;  //UserB:POT
        set:Variable.IPOExtn1 = 814201;         //IPOffice number
        set:Variable.IPOExtn2 = 201;
    }
    // T1
    if( $TestID == 12 ):
    {
        set:Variable.UserA = $x10_UserName;
        set:Variable.UserB = $x11_UserName;
        set:Variable.IncomingCallA_dssKey=4;   //UserA:LA01 - T1 TRUNK
        set:Variable.OutgoingCallB_dssKey=5;   //UserB:LA02 - T1 TRUNK
        set:Variable.IPOExtn1 = 201;           //IPOffice number
    }
    if( $TestID == 13 ):
    {
        set:Variable.UserA = $x19_UserName;
        set:Variable.UserB = $x20_UserName;
        set:Variable.IncomingCallA_dssKey=11;   //UserA:LA01 - T1 TRUNK
        set:Variable.OutgoingCallB_dssKey=1;    //UserB:LA02 - T1 TRUNK
        set:Variable.IPOExtn1 = 201;            //IPOffice number
    }
    if( $TestID == 14 ):
    {
        set:Variable.UserA = $x10_UserName;
        set:Variable.UserB = $x24_UserName;
        set:Variable.IncomingCallA_dssKey=4;  //UserA:LA01 - ANALOG TRUNK
        set:Variable.OutgoingCallB_dssKey=0;  //UserB:POT
        set:Variable.IPOExtn1 = 810201;         //IPOffice number
    }
    if( $TestID == 15 ):
    {
        set:Variable.UserA = $x10_UserName;
        set:Variable.UserB = $x14_UserName;
        set:Variable.IncomingCallA_dssKey=4;
        set:Variable.OutgoingCallB_dssKey=0;     //UserB:POT
        set:Variable.IPOExtn1 = 810201;         //IPOffice number
    }
    // Leave VM
    if( $TestID == 16 ):
    {
        set:Variable.UserA = $x19_UserName;
        set:Variable.ExtnA = $x19_UserNum;
        set:Variable.UserB = $x20_UserName;
        set:Variable.ExtnB = $x20_UserNum;
        set:Variable.Icom1A_dssKey=15;
        set:Variable.Icom2B_dssKey=5;
        set:Variable.Icom1B_dssKey=4;
    }
    // Listen VM
    if( $TestID == 17 ):
    {
        set:Variable.UserA = $x19_UserName;
        set:Variable.ExtnA = $x19_UserNum;
        set:Variable.UserB = $x20_UserName;
        set:Variable.ExtnB = $x20_UserNum;
        set:Variable.Icom1A_dssKey=15;
        set:Variable.Icom2B_dssKey=5;
        set:Variable.Icom1B_dssKey=4;
    }
    // Delete VM
    if( $TestID == 18 ):
    {
        set:Variable.UserA = $x19_UserName;
        set:Variable.ExtnA = $x19_UserNum;
        set:Variable.UserB = $x20_UserName;
        set:Variable.ExtnB = $x20_UserNum;
        set:Variable.Icom1A_dssKey=15;
        set:Variable.Icom2B_dssKey=5;
        set:Variable.Icom1B_dssKey=4;
    }
    // Save VM
    if( $TestID == 19 ):
    {
        set:Variable.UserA = $x19_UserName;
        set:Variable.ExtnA = $x19_UserNum;
        set:Variable.UserB = $x20_UserName;
        set:Variable.ExtnB = $x20_UserNum;
        set:Variable.Icom1A_dssKey=15;
        set:Variable.Icom2B_dssKey=5;
        set:Variable.Icom1B_dssKey=4;
    }

    // Assisted transfer
    if( $TestID == 20 ):
    {
        set:Variable.UserA = $x10_UserName;
        set:Variable.ExtnA = $x10_UserNum;
        set:Variable.UserB = $x11_UserName;
        set:Variable.ExtnB = $x11_UserNum;
        set:Variable.UserC = $x19_UserName;
        set:Variable.IncomingCall_dssKey=2;
        set:Variable.OutgoingCall_dssKey=12;
        set:Variable.Icom1_dssKey=0;
        set:Variable.Icom2_dssKey=1;
        set:Variable.IPOExtn1 = 209;
        set:Variable.IPOExtn2 = 210;
        set:Variable.TrunkID = 5; // Analog Trunk used to make incoming calls
    }
    // Not assisted transfer
    if( $TestID == 21 ):
    {
        set:Variable.UserA = $x10_UserName;
        set:Variable.ExtnA = $x10_UserNum;
        set:Variable.UserB = $x11_UserName;
        set:Variable.ExtnB = $x11_UserNum;
        set:Variable.UserC = $x19_UserName;
        set:Variable.IncomingCall_dssKey=2;
        set:Variable.OutgoingCall_dssKey=12;
        set:Variable.Icom1_dssKey=0;
        set:Variable.Icom2_dssKey=1;
        set:Variable.IPOExtn1 = 209;
        set:Variable.IPOExtn2 = 210;
        set:Variable.TrunkID = 5; // Analog Trunk used to make incoming calls
    }
    // 14xx phone display - Hold Call
    if( $TestID == 22 ):
    {
        set:Variable.UserA = $x19_UserName;
        set:Variable.UserB = $x20_UserName;
        set:Variable.ExtnA = $x19_UserNum;
        set:Variable.ExtnB = $x20_UserNum;
        set:Variable.IncomingCall_dssKey=5;
        set:Variable.OutgoingCall_dssKey=15;
    }
    // Conference
    if( $TestID == 23 ):
    {
        set:Variable.UserA = $x10_UserName;
        set:Variable.ExtnA = $x10_UserNum;
        set:Variable.UserB = $x11_UserName;
        set:Variable.ExtnB = $x11_UserNum;
        set:Variable.UserC = $x19_UserName;
        set:Variable.IncomingCall_dssKey=2;
        set:Variable.OutgoingCall_dssKey=12;
        set:Variable.Icom1_dssKey=0;
        set:Variable.Icom2_dssKey=1;
        set:Variable.IPOExtn1 = 209;
        set:Variable.IPOExtn2 = 210;
        set:Variable.TrunkID = 5; // Analog Trunk used to make incoming calls
    }

//////////////////////////////////////////////////////////////////////////////////
    // incoming call to extn57 - Analog Trunk
    if( $TestID == 24 ):
    {
        set:Variable.UserA = $x57_UserName;
        set:Variable.UserB = $x19_UserName;
        set:Variable.IncomingCallA_dssKey=6;     //UserA:LA01 - ANALOG TRUNK
        set:Variable.OutgoingCallB_dssKey=12;    //UserB:LA02 - ANALOG TRUNK
        set:Variable.IPOExtn1 = 209;             //IPOffice number
        set:Variable.IPOExtn2 = 210;             //IPOffice number
        set:Variable.TrunkID = 5; // Analog Trunk used to make incoming calls
    }
    // outgoing call from extn57 - Analog Trunk
    if( $TestID == 25 ):
    {
        set:Variable.UserA = $x19_UserName;
        set:Variable.UserB = $x57_UserName;
        set:Variable.IncomingCallA_dssKey=13;   //UserA:LA01 - ANALOG TRUNK
        set:Variable.OutgoingCallB_dssKey=7;    //UserB:LA02 - ANALOG TRUNK
        set:Variable.IPOExtn1 = 209;            //IPOffice number
        set:Variable.IPOExtn2 = 210;            //IPOffice number
        set:Variable.TrunkID = 5; // Analog Trunk used to make incoming calls
    }
    // incoming call to extn57 - SIP Trunk
    if( $TestID == 26 ):
    {
        set:Variable.UserA = $x57_UserName;
        set:Variable.UserB = $x19_UserName;
        set:Variable.ExtnA = $x57_UserNum;
        set:Variable.ExtnB = $x19_UserNum;
        set:Variable.IncomingCallA_dssKey=2;    //UserA:LA13 - SIP TRUNK
        set:Variable.OutgoingCallB_dssKey=8;    //UserB:LA14 - SIP TRUNK
        set:Variable.Icom1A_dssKey=4;           //UserA:Icom1 - SIP TRUNK
        set:Variable.Icom1B_dssKey=15;          //UserB:Icom1 - SIP TRUNK
        set:Variable.IPOExtn1 = 201;            //IPOffice number
    }
    // outgoing call from extn57 - SIP Trunk
    if( $TestID == 27 ):
    {
        set:Variable.UserA = $x19_UserName;
        set:Variable.UserB = $x57_UserName;
        set:Variable.ExtnA = $x19_UserNum;
        set:Variable.ExtnB = $x57_UserNum;
        set:Variable.IncomingCallA_dssKey=8;     //UserA:LA13 - SIP TRUNK
        set:Variable.OutgoingCallB_dssKey=2;     //UserB:LA14 - SIP TRUNK
        set:Variable.Icom1A_dssKey=15;           //UserA:Icom1 - SIP TRUNK
        set:Variable.Icom1B_dssKey=4;            //UserB:Icom1 - SIP TRUNK
        set:Variable.IPOExtn1 = 201;             //IPOffice number
    }
    // incoming call to extn57 - T1 Trunk
    if( $TestID == 28 ):
    {
        set:Variable.UserA = $x57_UserName;
        set:Variable.UserB = $x19_UserName;
        set:Variable.IncomingCallA_dssKey=0;     //UserA:LA09 - T1 TRUNK
        set:Variable.OutgoingCallB_dssKey=10;    //UserB:LA10 - T1 TRUNK
        set:Variable.IPOExtn1 = 201;            //IPOffice number
    }
    // outgoing call from extn57 - T1 Trunk
    if( $TestID == 29 ):
    {
        set:Variable.UserA = $x19_UserName;
        set:Variable.UserB = $x57_UserName;
        set:Variable.IncomingCallA_dssKey=11;   //UserA:LA09 - T1 TRUNK
        set:Variable.OutgoingCallB_dssKey=1;    //UserB:LA10 - T1 TRUNK
        set:Variable.IPOExtn1 = 201;            //IPOffice number
    }

    report(*** Finished doing phone configuration for test no: $TestID ***):<null>;
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

    wait:$wait_time;

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
    }
    // DIAL = user going offhook from IDLE state
    if( $State == "DIAL" ):
    {
        report(** DIAL ***):<null>;
        if( $PType == "ETR" ):
        {
            // check only first line is empty
            set:Variable.sa="                        ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for DIAL screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sa;

        }
        if( $PType == "1508" ):
        {
            set:Variable.sa="Dial: Number?           ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for DIAL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sa;
            set:Variable.sa="";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for DIAL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sa;
            set:Variable.sa="        Feature         ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for DIAL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sa;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sa="Dial: Number?           ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for DIAL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sa;
            set:Variable.sa="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for DIAL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sa;
            set:Variable.sa="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for DIAL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sa;
            set:Variable.sa="        Feature         ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for DIAL screen on line 3):User($Usr).cm_extn.DCP.Display[3]=$sa;
        }
    }
    // RING - State associated to user ringing when it is being called from an internal extension
    if( $State == "RING" ):
    {
        report(** RING ***):<null>;
        if( $PType == "ETR" ):
        {
            set:Variable.sb="$OtherExtn                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for RING screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sb;
            set:Variable.sb="                        ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for RING screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$sb;

        }
        if( $PType == "1508" ):
        {
            set:Variable.sb="Call: Incoming          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RING screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sb;
            set:Variable.sb="o%$OtherExtn             ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RING screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sb;
            set:Variable.sb="         To VM   Ignore ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RING screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sb;
        }
        // not verified - to be rebuilt
        if( $PType == "1516" ):
        {
            set:Variable.sb="Call: Incoming          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RING screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sb;
            set:Variable.sb="o%$OtherExtn             "
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RING screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sb;
            set:Variable.sb="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RING screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sb;
            set:Variable.sb="         To VM   Ignore ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RING screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sb;
        }
    }
    // EXT_RING - State associated to user ringing when it is being called from an external extension over Analog Trunk
    if( $State == "EXT_RING" ):
    {
        report(** EXT_RING ***):<null>;
        if( $PType == "ETR" ):
        {
            set:Variable.sc="$OtherExtn                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_RING screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sc;
            set:Variable.sc="Extn$OtherExtn                  ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_RING screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$sc;

        }
        if( $PType == "1508" ):
        {
            set:Variable.sc="Call: Incoming          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RING screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sc;
            set:Variable.sc="o%Extn$OtherExtn             ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RING screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sc;
            set:Variable.sc="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RING screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sc;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sc="Call: Incoming          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sc;
            set:Variable.sc="o%Extn$OtherExtn             ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sc;
            set:Variable.sc="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sc;
            set:Variable.sc="                 Ignore ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sc;
        }
    }

    // EXT_RING_SIP - State associated to user ringing when it is being called from an external extension over SIP Trunk
    if( $State == "EXT_RING_SIP" ):
    {
        report(** EXT_RING_SIP ***):<null>;
        if( $PType == "ETR" ):
        {
            set:Variable.sd="$OtherExtn                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_RING_SIP screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sd;
            set:Variable.sd="                        ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_RING_SIP screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$sd;
        }
        // not verified for 1508 - to be built
        if( $PType == "1508" ):
        {
            set:Variable.sd="Call: Incoming          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RING_SIP screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sd;
            set:Variable.sd="o%$OtherExtn            ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RING_SIP screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sd;
            set:Variable.sd="                 Ignore ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RING_SIP screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sd;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sd="Call: Incoming          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING_SIP screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sd;
            set:Variable.sd="o%$OtherExtn             ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING_SIP screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sd;
            set:Variable.sd="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING_SIP screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sd;
            set:Variable.sd="                 Ignore ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING_SIP screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sd;
        }
    }
    // EXT_RING_EXTERNAL - State associated to user ringing when it is being called from an external extension over PRI/T1 Trunk
    if( $State == "EXT_RING_EXTERNAL" ):
    {
        report(** EXT_RING_EXTERNAL ***):<null>;
        if( $PType == "ETR" ):
        {
            set:Variable.se="External              ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$se;
            set:Variable.se="                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$se;
        }
        if( $PType == "1508" ):
        {
            set:Variable.se="Call: Incoming          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$se;
            set:Variable.se="o%External              ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$se;
            set:Variable.se="                 Ignore ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$se;
        }
        if( $PType == "1516" ):
        {
            set:Variable.se="Call: Incoming          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$se;
            set:Variable.se="o%External              ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$se;
            set:Variable.se="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$se;
            set:Variable.se="                 Ignore ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RING_EXTERNAL screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$se;
        }
    }
    //ENQUIRE_RING - State associated to user making an enquiry call to transfer an existing external connected call
    if( $State == "ENQUIRE_RING" ):
    {
        report(** ENQUIRE RING ***):<null>;
        if( $PType == "ETR" ):
        {
            // phone has two lines
            set:Variable.sf="$OExt1";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for ENQUIRE_RING screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sf;
            set:Variable.sf="Extn$OExt1($OExt2)";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for ENQUIRE_RING screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$sf;
        }
        // not verified - to be rebuilt
        if( $PType == "1508" ):
        {
            // Phone has three lines
            set:Variable.sf="Conn:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for ENQUIRE_RING screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sf;
            set:Variable.sf="v|Voicemail";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for ENQUIRE_RING screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sf;
            set:Variable.sf="        Feature  Admin  ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for ENQUIRE_RING screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sf;
        }
        // not verified - to be rebuilt
        if( $PType == "1516" ):
        {
            // Phone has four lines
            set:Variable.sf="Conn:                   ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for ENQUIRE_RING screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sf;
            set:Variable.sf="v|Voicemail             ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for ENQUIRE_RING screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sf;
            set:Variable.sf="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for ENQUIRE_RING screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sf;
            set:Variable.sf="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for ENQUIRE_RING screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sf;
        }
    }
    //RINGBACK - State associated to user calling another internal extension
    if( $State == "RINGBACK" ):
    {
        report(** RINGBACK ***):<null>;
        if( $PType == "ETR" ):
        {
            set:Variable.sg="$OtherExtn                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for RINGBACK screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sg;
        }
        // not verified - must be rebuilt
        if( $PType == "1508" ):
        {
            set:Variable.sg="Call:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RINGBACK screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sg;
            set:Variable.sg="v|$OtherExtn            ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RINGBACK screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sg;
            set:Variable.sg=" AutCB                  ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RINGBACK screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sg;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sg="Call:                   ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RINGBACK screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sg;
            set:Variable.sg="v|$OtherExtn            ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RINGBACK screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sg;
            set:Variable.sg="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RINGBACK screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sg;
            set:Variable.sg=" AutCB                  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RINGBACK screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sg;
        }
    }
    //EXT_RINGBACK - State associated to user calling an external extension over Analog Trunk
    if( $State == "EXT_RINGBACK" ):
    {
        report(** EXT_RINGBACK ***):<null>;
        // not verified - to be rebuilt
        if( $PType == "ETR" ):
        {
            set:Variable.sh="$OtherExtn                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_RINGBACK screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sh;
        }
        if( $PType == "1508" ):
        {
            set:Variable.sh="Conn:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RINGBACK screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sh;
            set:Variable.sh="o|External              ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RINGBACK screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sh;
            set:Variable.sh="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RINGBACK screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sh;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sh="Conn:                   ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RINGBACK screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sh;
            set:Variable.sh="o|External            ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RINGBACK screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sh;
            set:Variable.sh="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RINGBACK screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sh;
            set:Variable.sh="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RINGBACK screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sh;
        }
    }
    //EXT_RINGBACK_CALL - State associated to user calling an external extension over PRI/T1 Trunk
    if( $State == "EXT_RINGBACK_CALL" ):
    {
        report(** EXT_RINGBACK_CALL ***):<null>;

        if( $PType == "ETR" ):
        {
            set:Variable.si="$OtherExtn                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$si;
        }
        if( $PType == "1508" ):
        {
            set:Variable.si="Call:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$si;
            set:Variable.si="o|$OtherExtn            ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$si;
            set:Variable.si="                        ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$si;
        }
        // not verified - to be rebuilt
        if( $PType == "1516" ):
        {
            set:Variable.si="Call:                   ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$si;
            set:Variable.si="o|$OtherExtn    ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$si;
            set:Variable.si="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$si;
            set:Variable.si="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_RINGBACK_CALL screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$si;
        }
    }
    //CONN - State associated to user connected to another internal extension
    if( $State == "CONN" ):
    {
        report(** CONN ***):<null>;
        if( $PType == "ETR" ):
        {

            set:Variable.sj="$OtherExtn                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for CONN screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sj;
        }
        if( $PType == "1508" ):
        {
            set:Variable.sj="Conn:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CONN screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sj;
            //set:Variable.sj="o|                      ";
            //verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CONN screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sj;
            set:Variable.sj="$OtherExtn                    >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CONN screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sj;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sj="Conn:                  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONN screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sj;
            //set:Variable.sj="v|                     ";
            //verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONN screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sj;
            set:Variable.sj="$OtherExtn             ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONN screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sj;
            set:Variable.sj="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONN screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sj;
        }
    }
    //EXT_CALLER_CONN -  State associated to user connected to external user over Analog Trunk - user is calling
    if( $State == "EXT_CALLER_CONN" ):
    {
        report(** EXT_CALLER_CONN ***):<null>;
        if( $PType == "ETR" ):
        {
            set:Variable.sk="$OtherExtn                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_CALLER_CONN screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sk;
        }
        if( $PType == "1508" ):
        {
            set:Variable.sk="Conn:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CALLER_CONN screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sk;
            set:Variable.sk="o|External              ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CALLER_CONN screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sk;
            set:Variable.sk="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CALLER_CONN screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sk;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sk="Conn:                  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CALLER_CONN screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sk;
            set:Variable.sk="o|External             ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CALLER_CONN screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sk;
            set:Variable.sk="$OtherExtn             ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CALLER_CONN screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sk;
            set:Variable.sk="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CALLER_CONN screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sk;
        }
    }
    //EXT_CALLED_CALL -  State associated to user called by external user over Analog Trunk - user is being called
    if( $State == "EXT_CALLED_CALL" ):
    {
        report(** EXT_CALLED_CALL ***):<null>;
        if( $PType == "ETR" ):
        {
            set:Variable.sl="$OtherExtn                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_CALLED_CALL screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sl;
        }
        if( $PType == "1508" ):
        {
            set:Variable.sl="Call:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CALLED_CALL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sl;
            set:Variable.sl="o|Extn$OtherExtn   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CALLED_CALL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sl;
            set:Variable.sl="";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CALLED_CALL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sl;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sl="Call:                  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CALLED_CALL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sl;
            set:Variable.sl="o|Extn$OtherExtn   ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CALLED_CALL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sl;
            set:Variable.sl="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CALLED_CALL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sl;
            set:Variable.sl="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CALLED_CALL screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sl;
        }
    }
    //EXT_CALLED_CONN -  State associated to user called by external user over Analog Trunk - user is being called
    if( $State == "EXT_CALLED_CONN" ):
    {
        report(** EXT_CALLED_CONN ***):<null>;
        if( $PType == "ETR" ):
        {
            set:Variable.sm="$OtherExtn                      ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_CALLED_CONN screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line;
        }
        if( $PType == "1508" ):
        {
            set:Variable.sm="Conn:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CALLED_CONN screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sm;
            set:Variable.sm="o|Extn$OtherExtn        ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CALLED_CONN screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sm;
            set:Variable.sm="$OtherExtn              ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CALLED_CONN screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sm;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sm="Conn:                  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CALLED_CONN screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sm;
            set:Variable.sm="o|Extn$OtherExtn       ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CALLED_CONN screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sm;
            set:Variable.sm="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CALLED_CONN screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sm;
            set:Variable.sm="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CALLED_CONN screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sm;
        }
    }
    //EXT_RINGBACK_CALL - State associated to user connected to an external extension over PRI/T1 Trunk
    if( $State == "EXT_CONN_EXTERNAL" ):
    {
        report(** EXT_CONN_EXTERNAL ***):<null>;

        if( $PType == "ETR" ):
        {
            set:Variable.sn="External";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sn;
        }
        // not verified - to be rebuilt
        if( $PType == "1508" ):
        {
            set:Variable.sn="Conn:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sn;
            set:Variable.sn="o|External        ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sn;
            set:Variable.sn="        Feature  Admin  ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sn;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sn="Conn:            ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sn;
            set:Variable.sn="o|External        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sn;
            set:Variable.sn="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sn;
            set:Variable.sn="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for EXT_CONN_EXTERNAL screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sn;
        }
    }
    //F590 - State associated to user dialling Feature 590
    if( $State == "F590" ):
    {
        report(** F590 ***):<null>;
        // not verified - to be rebuilt
        if( $PType == "ETR" ):
        {
            set:Variable.so="BEP 8.1";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for F590 screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$so;
        }
        // not verified - to be rebuilt
        if( $PType == "1508" ):
        {
            set:Variable.so="Conn:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F590 screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$so;
            set:Variable.so="o|Extn$OtherExtn        ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F590 screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$so;
            set:Variable.so="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F590 screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$so;
        }
        if( $PType == "1516" ):
        {
            set:Variable.so="BEP 8.1";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F590 screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$so;
            set:Variable.so="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F590 screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$so;
            set:Variable.so="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F590 screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$so;
            set:Variable.so="                  Exit  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F590 screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$so;
        }
    }
    //F591 - State associated to user dialling Feature 591
    if( $State == "F591" ):
    {
        report(** F591 ***):<null>;
        // not verified - to be rebuilt
        if( $PType == "ETR" ):
        {
            set:Variable.sp="$OtherExtn";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for F591 screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sp;
        }
        // not verified - to be rebuilt
        if( $PType == "1508" ):
        {
            set:Variable.sp="$OtherExtn";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F591 screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sp;
            set:Variable.sp="o|Extn$OtherExtn        ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F591 screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sp;
            set:Variable.sp="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F591 screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sp;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sp="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F591 screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sp;
            set:Variable.sp="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F591 screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sp;
            set:Variable.sp="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F591 screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sp;
            set:Variable.sp="                  Exit  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F591 screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sp;
        }
    }
    //VM_CONN - State associated to user connected to mailbox
    if( $State == "VM_CONN" ):
    {
        report(** VM_CONN ***):<null>;
        if( $PType == "ETR" ):
        {
            set:Variable.sq="?$Usr";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for VM_CONN screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sq;
        }
        if( $PType == "1508" ):
        {
            set:Variable.sq="Conn:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for VM_CONN screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sq;
            set:Variable.sq="v|Voicemail";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for VM_CONN screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sq;
            set:Variable.sq="        Feature  Admin  ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for VM_CONN screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sq;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sq="Conn:                   ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for VM_CONN screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sq;
            set:Variable.sq="v|Voicemail             ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for VM_CONN screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sq;
            set:Variable.sq="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for VM_CONN screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sq;
            set:Variable.sq="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for VM_CONN screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sq;
        }
    }
    //HOLD - State associated to user who puts on hold another internal user
    if( $State == "HOLD" ):
    {
        report(** HOLD ***):<null>;
        // not verified - to be rebuilt
        if( $PType == "ETR" ):
        {
            set:Variable.sr="";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for HOLD screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sr;
        }
        if( $PType == "1508" ):
        {
            set:Variable.sr="Call: On-Hold           ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HOLD screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sr;
            set:Variable.sr="o";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HOLD screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sr;
            set:Variable.sr="$OtherExtn                    >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HOLD screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sr;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sr="Call: On-Hold           ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HOLD screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sr;
            set:Variable.sr="v";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HOLD screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sr;
            set:Variable.sr="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HOLD screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sr;
            set:Variable.sr=" Pickup             ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HOLD screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sr;
        }
    }
    //HELD - State associated to user who is put on hold by another internal user
    if( $State == "HELD" ):
    {
        report(** HELD ***):<null>;
        // not verified - to be rebuilt
        if( $PType == "ETR" ):
        {
            set:Variable.st="";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for HELD screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$st;
        }
        if( $PType == "1508" ):
        {
            set:Variable.st="Held:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HELD screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$st;
            set:Variable.st="o";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HELD screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$st;
            set:Variable.st="$OtherExtn                    >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HELD screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$st;
        }
        if( $PType == "1516" ):
        {
            set:Variable.st="Held:                  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HELD screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$st;
            set:Variable.st="v|                      ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HELD screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$st;
            set:Variable.st="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HELD screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$st;
            set:Variable.st="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HELD screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$st;
        }
    }
    //CONF - State associated to user being involved in a conference - CONF 100
    if( $State == "CONF" ):
    {
        report(** CONF ***):<null>;
        if( $PType == "ETR" ):
        {
            set:Variable.su="Conf 100                ";
            verify(Display Verification Issue: ETR User: $Usr has incorrect info for CONF screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$su;

        }
        // not verified - to be rebuilt
        if( $PType == "1508" ):
        {
            set:Variable.su="Call: Incoming          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CONF screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$su;
            set:Variable.su="o%$OtherExtn             ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CONF screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$su;
            set:Variable.su="         To VM   Ignore ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CONF screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$su;
        }
        // not verified - to be rebuilt
        if( $PType == "1516" ):
        {
            set:Variable.su="Call: Incoming          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONF screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$su;
            set:Variable.su="o%$OtherExtn             "
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONF screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$su;
            set:Variable.su="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONF screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$su;
            set:Variable.su="         To VM   Ignore ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONF screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$su;
        }
    }

    report(*** FINISHED: Display verification for User: $Usr ***):<null>;
}

////////////////////// MAPDSSKEY /////////////////////////////////////////////
MapDSSKey:
{
    report(*** STARTED: Mapping DSS Keys for User: $Usr ***):<null>;
    report(*** Phone Type: $PType ***):<null>;

    // ETR phone
    if( $IsSage == False ):
    {
        set:Variable.Icom1 = 0;   // Intercom1
        set:Variable.Icom2 = 1;   // Intercom2
        set:Variable.LA1 = 2;     // LA01 - Analog Trunk
        set:Variable.LA2 = 3;     // LA02 - Analog Trunk
        set:Variable.LA9 = 4;     // LA09 - PRI/T1 Trunk
        set:Variable.LA10 = 5;    // LA10 - PRI/T1 Trunk
        set:Variable.LA17 = 6;    // LA17 - SIP Trunk
        set:Variable.LA18 = 7;    // LA18 - SIP Trunk
    }
    // 14xx phone
    if( $IsSage == True ):
    {
        if( $PType == "1508" ):
        {
            set:Variable.Icom1 = 4;   // Intercom1
            set:Variable.Icom2 = 5;   // Intercom2
            set:Variable.LA1 = 6;     // LA01 - Analog Trunk
            set:Variable.LA2 = 7;     // LA02 - Analog Trunk
            set:Variable.LA9 = 0;     // LA09 - PRI/T1 Trunk
            set:Variable.LA10 = 1;    // LA10 - PRI/T1 Trunk
            set:Variable.LA17 = 2;    // LA17 - SIP/T1 Trunk
            set:Variable.LA18 = 3;    // LA18 - SIP/T1 Trunk
        }
        if( $PType == "1516" ):
        {
            set:Variable.Icom1 = 15;   // Intercom1
            set:Variable.Icom2 = 14;   // Intercom2
            set:Variable.LA1 = 13;     // LA01 - Analog Trunk
            set:Variable.LA2 = 12;     // LA02 - Analog Trunk
            set:Variable.LA9 = 11;     // LA09 - PRI/T1 Trunk
            set:Variable.LA10 = 10;    // LA10 - PRI/T1 Trunk
            set:Variable.LA17 = 9;    // LA17 - SIP Trunk
            set:Variable.LA18 = 8;    // LA18 - SIP Trunk
        }
    }

    report(*** STARTED: Finished mapping DSS Keys for User: $Usr ***):<null>;
}

////////////////////////// Make Incoming Analog Call //////////////////////////
MakeICAlogTrunkCall:
{
    set:CfgLine($TrunkID).cm_line.AlogTrunk.Rx =
    {
        command=CMSetup;
        calling_party.number = $IPOExtn2;
        calling_party.type = CMNTypeDefault;
        calling_party.plan = CMNPlanDefault;
        calling_party.pres = CMNPresDefault;
        calling_party.screen = CMNScreenDefault;
        calling_party_name = Extn$IPOExtn2;
    }
}
////////////////////// Clear Incoming Analog Call /////////////////////////////
ClearICAlogTrunkCall:
{
    report(*** Release Trunk ***):<null>;
    set:CfgLine($TrunkID).cm_line.AlogTrunk.Rx =
    {
        command=CMReleaseComp;
        cause=CMCauseNormal;
    }
    report(*** End Clearing Analog Trunk ***):<null>;
}
///////////////////////////////////////////////////////////////////////////////
