////////////////////////////////////////////////////////////////////////////////
// ----------------------------------------------------------------------------
// ..\..\Partner\AcceptanceBRI.tst
//
// Script for Partner Acceptance run against BRI configurations
//
// Duration to run on target: 25min
//
// Modification History
// YYMMDD Name                    Comment
// 111107 Mihai Manolache         Initial Creation
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
        wait:200000;
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
    set:Variable.TestEnd=30;
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
// Acceptance - Test1                                                   //
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
// Acceptance - Test2                                              //
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
// Acceptance - Test3                                              //
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
//////////////////////////////////////////////////////////////////////
// Acceptance - Test4                                               //
//    SCENARIO : keywords=BRI Trunk – Outgoing call – 14xx          //
//      Originator phone type: 1408                                 //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase4:
{
    report(********** TestCase4 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoing14XXCallBRI;
    gosub:Deconfiguration;
    report(********** TestCase4 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test5                                               //
//    SCENARIO : keywords=BRI Trunk – Incoming call – 14xx          //
//      Originator phone type: 1416                                 //
//      Destination phone type: 1408                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase5:
{
    report(********** TestCase5 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicIncoming14XXCallBRI;
    gosub:Deconfiguration;
    report(********** TestCase5 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test6                                               //
//    SCENARIO : keywords=BRI Trunk – Outgoing call – 95xx          //
//      Originator phone type: 95xx                                 //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase6:
{
    report(********** TestCase6 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoing95XXCallBRI;
    gosub:Deconfiguration;
    report(********** TestCase6 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test7                                               //
//    SCENARIO : keywords=BRI Trunk – Incoming call – 95xx          //
//      Originator phone type: 1416                                 //
//      Destination phone type: 95xx                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase7:
{
    report(********** TestCase7 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicIncoming95XXCallBRI;
    gosub:Deconfiguration;
    report(********** TestCase7 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test8                                               //
//    SCENARIO : keywords=BRI Trunk – Outgoing call – Nortel T Series//
//      Originator phone type: T7316E                                 //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase8:
{
    report(********** TestCase8 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingNortelCallBRI;
    gosub:Deconfiguration;
    report(********** TestCase8 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test9                                               //
//    SCENARIO : keywords=BRI Trunk – Incoming call – Nortel T Series//
//      Originator phone type: 1416                                 //
//      Destination phone type: T7316E                               //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase9:
{
    report(********** TestCase9 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicIncomingNortelCallBRI;
    gosub:Deconfiguration;
    report(********** TestCase9 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test10                                               //
//    SCENARIO : keywords=BRI Trunk – Outgoing call – Nortel M Series//
//      Originator phone type: M7324                                //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase10:
{
    report(********** TestCase10 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingNortelCallBRI;
    gosub:Deconfiguration;
    report(********** TestCase10 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test11                                               //
//    SCENARIO : keywords=BRI Trunk – Incoming call – Nortel M Series//
//      Originator phone type: 1416                                 //
//      Destination phone type: M7324                               //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase11:
{
    report(********** TestCase11 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicIncomingNortelCallBRI;
    gosub:Deconfiguration;
    report(********** TestCase11 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test12                                               //
//    SCENARIO : keywords=BRI Trunk – Outgoing call – POTS          //
//      Originator phone type: POTS                                 //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase12:
{
    report(********** TestCase12 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingPOTSCallBRI;
    gosub:Deconfiguration;
    report(********** TestCase12 COMPLETED **********):<null>;
}

//////////////////////////////////////////////////////////////////////
// Acceptance - Test13                                               //
//    SCENARIO : keywords=SIP Trunk – Outgoing call – 14xx          //
//      Originator phone type: 1408                                 //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase13:
{
    report(********** TestCase13 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoing14XXCallSIP;
    gosub:Deconfiguration;
    report(********** TestCase13 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test14                                               //
//    SCENARIO : keywords=SIP Trunk – Incoming call – 14xx          //
//      Originator phone type: 1416                                 //
//      Destination phone type: 1408                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase14:
{
    report(********** TestCase14 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicIncoming14XXCallSIP;
    gosub:Deconfiguration;
    report(********** TestCase14 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test15                                               //
//    SCENARIO : keywords=SIP Trunk – Outgoing call – 95xx          //
//      Originator phone type: 95xx                                 //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase15:
{
    report(********** TestCase15 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoing95XXCallSIP;
    gosub:Deconfiguration;
    report(********** TestCase15 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test16                                               //
//    SCENARIO : keywords=SIP Trunk – Incoming call – 95xx          //
//      Originator phone type: 1416                                 //
//      Destination phone type: 95xx                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase16:
{
    report(********** TestCase16 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicIncoming95XXCallSIP;
    gosub:Deconfiguration;
    report(********** TestCase16 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test17                                               //
//    SCENARIO : keywords=SIP Trunk – Outgoing call – Nortel T Series//
//      Originator phone type: T7316E                                 //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase17:
{
    report(********** TestCase17 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingNortelCallSIP;
    gosub:Deconfiguration;
    report(********** TestCase17 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test18                                               //
//    SCENARIO : keywords=SIP Trunk – Incoming call – Nortel T Series//
//      Originator phone type: 1416                                 //
//      Destination phone type: T7316E                               //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase18:
{
    report(********** TestCase18 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicIncomingNortelCallSIP;
    gosub:Deconfiguration;
    report(********** TestCase18 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test19                                               //
//    SCENARIO : keywords=SIP Trunk – Outgoing call – Nortel M Series//
//      Originator phone type: M7324                                //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase19:
{
    report(********** TestCase19 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingNortelCallSIP;
    gosub:Deconfiguration;
    report(********** TestCase19 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test20                                               //
//    SCENARIO : keywords=SIP Trunk – Incoming call – Nortel M Series//
//      Originator phone type: 1416                                 //
//      Destination phone type: M7324                               //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase20:
{
    report(********** TestCase20 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicIncomingNortelCallSIP;
    gosub:Deconfiguration;
    report(********** TestCase20 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test21                                               //
//    SCENARIO : keywords=SIP Trunk – Outgoing call – POTS          //
//      Originator phone type: POTS                                 //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase21:
{
    report(********** TestCase21 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingPOTSCallSIP;
    gosub:Deconfiguration;
    report(********** TestCase21 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test22                                               //
//    SCENARIO : keywords=ANALOG Trunk – Outgoing call – 14xx          //
//      Originator phone type: 1408                                 //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase22:
{
    report(********** TestCase22 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoing14XXCallANALOG;
    gosub:Deconfiguration;
    report(********** TestCase22 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test23                                               //
//    SCENARIO : keywords=ANALOG Trunk – Incoming call – 14xx          //
//      Originator phone type: 1416                                 //
//      Destination phone type: 1408                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase23:
{
    report(********** TestCase23 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicIncoming14XXCallANALOG;
    gosub:Deconfiguration;
    report(********** TestCase23 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test24                                               //
//    SCENARIO : keywords=ANALOG Trunk – Outgoing call – 95xx          //
//      Originator phone type: 95xx                                 //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase24:
{
    report(********** TestCase24 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoing95XXCallANALOG;
    gosub:Deconfiguration;
    report(********** TestCase24 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test25                                               //
//    SCENARIO : keywords=ANALOG Trunk – Incoming call – 95xx          //
//      Originator phone type: 1416                                 //
//      Destination phone type: 95xx                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase25:
{
    report(********** TestCase25 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicIncoming95XXCallANALOG;
    gosub:Deconfiguration;
    report(********** TestCase25 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test26                                               //
//    SCENARIO : keywords=ANALOG Trunk – Outgoing call – Nortel T Series//
//      Originator phone type: T7316E                                 //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase26:
{
    report(********** TestCase26 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingNortelCallANALOG;
    gosub:Deconfiguration;
    report(********** TestCase26 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test27                                               //
//    SCENARIO : keywords=ANALOG Trunk – Incoming call – Nortel T Series//
//      Originator phone type: 1416                                 //
//      Destination phone type: T7316E                               //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase27:
{
    report(********** TestCase27 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicIncomingNortelCallANALOG;
    gosub:Deconfiguration;
    report(********** TestCase27 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test28                                               //
//    SCENARIO : keywords=ANALOG Trunk – Outgoing call – Nortel M Series//
//      Originator phone type: M7324                                //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase28:
{
    report(********** TestCase28 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingNortelCallANALOG;
    gosub:Deconfiguration;
    report(********** TestCase28 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test29                                               //
//    SCENARIO : keywords=ANALOG Trunk – Incoming call – Nortel M Series//
//      Originator phone type: 1416                                 //
//      Destination phone type: M7324                               //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase29:
{
    report(********** TestCase29 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicIncomingNortelCallANALOG;
    gosub:Deconfiguration;
    report(********** TestCase29 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////
// Acceptance - Test30                                               //
//    SCENARIO : keywords=ANALOG Trunk – Outgoing call – POTS          //
//      Originator phone type: POTS                                 //
//      Destination phone type: 1416                                //
//                                                                  //
//////////////////////////////////////////////////////////////////////
TestCase30:
{
    report(********** TestCase30 STARTED **********):<null>;
    gosub:Configuration;
    gosub:TestBasicOutgoingPOTSCallANALOG;
    gosub:Deconfiguration;
    report(********** TestCase30 COMPLETED **********):<null>;
}
//////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////
// Acceptance - CALL SCRIPTS                   //
/////////////////////////////////////////////////
TestBasicUpgrade:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User C IDLE
    set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallC_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B offhook
        set:User($UserB).cm_extn.DCP.HookChange = OffHook;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
        verify(Tone Verification Issue: $UserB is not in dialing state):User($UserB).cm_extn.current_ep.state=CMCSDialling;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_ANALOG";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "CALLING_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // User C Ringing
    set:Variable.Usr = $UserC;set:Variable.State = "CALLED_ANALOG";set:Variable.PType = "Nortel";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallC_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_ANALOG";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // User C Idle
    set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PhoneType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallC_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
    if($RunMode == Rig):
    {
	      set:User($UserB).cm_extn.DCP.HookChange = OnHook;
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
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B Idle
        set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCall_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // User C Idle
    set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PhoneType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallC_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
}

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

    // User A dials Feature 592 on idle screen
    report( - PressSoftKey <Feature> - ):<null>;
    set:User($UserA).cm_extn.DCP.MenuKey=B;
    wait:$wait_time;
    set:User($UserA).cm_extn.DCP.StdKey =5;
    set:User($UserA).cm_extn.DCP.StdKey =9;
    set:User($UserA).cm_extn.DCP.StdKey =2;
    wait:$delay_time;

    // Check Display for A
    set:Variable.Usr = $UserA;set:Variable.State = "F592";set:Variable.PType = "1516";set:Variable.OtherExtn=$PartnerIP;
    gosub:CheckDisplay;

    // User A exits
    report( - PressSoftKey <Exit> - ):<null>;
    set:User($UserA).cm_extn.DCP.MenuKey=C;
    wait:$delay_time;

    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
}

TestBasicEmbeddedVM:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User C IDLE
    set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallC_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A offhook
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;
    wait:$delay_time;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSDialling;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneDial;
    wait:$delay_time;

    // User A DIAL
    set:Variable.Usr = $UserA;set:Variable.State = "DIAL";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A dials 777
    set:User($UserA).cm_extn.DialWithGaps.1000=777;
    wait:$delay_time;

    // User A connected to VM
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state = CMCSConnected;
    //commented this because VMail object cannot be used properly
    //sync($sync_delay_time):VMail($ExtnA).state = CMCSConnected;

    // Check display for A connected to VM
    set:Variable.Usr = $UserA;set:Variable.State = "VM_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;
    wait:$wait_time;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.GetActiveTone=CMLocalToneDial;
    wait:$delay_time;

    // User B DIAL
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B dials 777
    set:User($UserB).cm_extn.DialWithGaps.1000=777;
    wait:$delay_time;

    // User B connected to VM
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state = CMCSConnected;
    //commented this because VMail object cannot be used properly
    //sync($sync_delay_time):VMail($ExtnB).state = CMCSConnected;

    // Check display for B connected to VM
    set:Variable.Usr = $UserB;set:Variable.State = "VM_CONN";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;
    wait:$wait_time;

    // User C offhook
    set:User($UserC).cm_extn.DCP.HookChange = OffHook;
    sync($sync_delay_time):User($UserC).cm_extn.current_ep.state=CMCSDialling;
    sync($sync_delay_time):User($UserC).cm_extn.current_ep.GetActiveTone=CMLocalToneDial;
    wait:$delay_time;

    // User C DIAL
    set:Variable.Usr = $UserC;set:Variable.State = "DIAL";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallC_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User C dials 777
    set:User($UserC).cm_extn.DialWithGaps.1000=777;
    wait:$delay_time;

    // User C gets ringback tone from VM
    sync($sync_delay_time):User($UserC).cm_extn.current_ep.state = CMCSRingBack;

    // Check display for C in ringback state
    set:Variable.Usr = $UserC;set:Variable.State = "RINGBACK";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallC_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
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

    // User A CONNECTED
    set:Variable.Usr = $UserA;set:Variable.State = "VM_CONN";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User C CONNECTED
    set:Variable.Usr = $UserC;set:Variable.State = "VM_CONN";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallC_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
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
    set:Variable.Btn = $VMCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User C Idle
    set:Variable.Usr = $UserC;set:Variable.State = "IDLE";set:Variable.PhoneType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $VMCallC_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
}

TestBasicOutgoing14XXCallBRI:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_BRI";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_BRI";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_BRI";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;

    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_BRI";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
}

TestBasicIncoming14XXCallBRI:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    verify(Tone Verification Issue: $UserB is not in dialing state):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_BRI";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_BRI";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_BRI";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn2;

    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_BRI";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
}

TestBasicOutgoing95XXCallBRI:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    verify(Tone Verification Issue: $UserB is not in dialing state):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_BRI";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_BRI";set:Variable.PType = "9508";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_BRI";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;

    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_BRI";set:Variable.PType = "9508";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
}

TestBasicIncoming95XXCallBRI:
{
    wait:$delay_time;
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_BRI";set:Variable.PType = "9508";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_BRI";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_BRI";set:Variable.PType = "9508";set:Variable.OtherExtn=$IPOExtn2;

    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_BRI";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
}

TestBasicOutgoingNortelCallBRI:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    verify(Tone Verification Issue: $UserB is not in dialing state):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_BRI";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_BRI";set:Variable.PType = "Nortel";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_BRI";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;

    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_BRI";set:Variable.PType = "Nortel";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
}

TestBasicIncomingNortelCallBRI:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_BRI";set:Variable.PType = "Nortel";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_BRI";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_BRI";set:Variable.PType = "Nortel";set:Variable.OtherExtn=$IPOExtn2;

    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_BRI";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
}

TestBasicOutgoingPOTSCallBRI:
{
    // -----------------------------------------
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE (POTS) - no check

    // User B offhook
    set:User($UserB).cm_extn.FlashHook = True;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    verify(Tone Verification Issue: $UserB is not in dialing state):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // User B IDLE (POTS) - no check

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_BRI";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Connected (POTS) - no check

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSOGConnReq;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_BRI";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Connected (POTS) - no check

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserB).cm_extn.OnHook;
	  wait:1000;
    set:User($UserB).cm_extn.OnHook;
	  wait:1000;
    set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle (POTS) - no check

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    //sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
}

//////////////////////////////////////////////////////////////////////////////////////////////////
TestBasicOutgoing14XXCallSIP:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_SIP";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;

    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_SIP";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn3;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
}

TestBasicIncoming14XXCallSIP:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_SIP";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_SIP";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn2;

    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn3;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
}

TestBasicOutgoing95XXCallSIP:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_SIP";set:Variable.PType = "9508";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;

    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_SIP";set:Variable.PType = "9508";set:Variable.OtherExtn=$IPOExtn3;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
}

TestBasicIncoming95XXCallSIP:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_SIP";set:Variable.PType = "9508";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_SIP";set:Variable.PType = "9508";set:Variable.OtherExtn=$IPOExtn2;

    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn3;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
}

TestBasicOutgoingNortelCallSIP:
{
    wait:$delay_time;
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_SIP";set:Variable.PType = "Nortel";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;

    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_SIP";set:Variable.PType = "Nortel";set:Variable.OtherExtn=$IPOExtn3;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
}

TestBasicIncomingNortelCallSIP:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B offhook
    set:User($UserB).cm_extn.DCP.HookChange = OffHook;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // Check DIAL display and lamps for B
    set:Variable.Usr = $UserB;set:Variable.State = "DIAL";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey; set:Variable.GreenLp ="On"; set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_SIP";set:Variable.PType = "Nortel";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_SIP";set:Variable.PType = "Nortel";set:Variable.OtherExtn=$IPOExtn2;

    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B connected
    set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn3;
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;
}


TestBasicOutgoingPOTSCallSIP:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE (POTS) - no check

    // User B offhook
    set:User($UserB).cm_extn.FlashHook = True;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    verify(Tone Verification Issue: $UserB is not in dialing state):User($UserB).cm_extn.current_ep.state=CMCSDialling;
    wait:$delay_time;

    // User B IDLE (POTS) - no check

    // B dials external number
    set:User($UserB).cm_extn.DialWithGaps.1000=$IPOExtn1;

    wait:$ring_time;

    // User A&C are ringing
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSRinging;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSRingBack;

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Connected (POTS) - no check

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSOGConnReq;

    // Talkpath between A & B
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_SIP";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Connected (POTS) - no check

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserB).cm_extn.OnHook;
	  wait:1000;
    set:User($UserB).cm_extn.OnHook;
	  wait:1000;
    set:User($UserB).cm_extn.OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    //sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle (POTS) - no check
}

//////////////////////////////////////////////////////////////////////////////////////////////////
TestBasicOutgoing14XXCallANALOG:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B offhook
        set:User($UserB).cm_extn.DCP.HookChange = OffHook;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
        wait:$delay_time;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "CALLING_ANALOG";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_ANALOG";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

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
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B Idle
        set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }
}

TestBasicIncoming14XXCallANALOG:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B offhook
        set:User($UserB).cm_extn.DCP.HookChange = OffHook;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
        wait:$delay_time;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_ANALOG";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "CALLING_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_ANALOG";set:Variable.PType = "1508";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

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
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B Idle
        set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }
}

TestBasicOutgoing95XXCallANALOG:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B offhook
        set:User($UserB).cm_extn.DCP.HookChange = OffHook;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
        wait:$delay_time;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "CALLING_ANALOG";set:Variable.PType = "9508";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_ANALOG";set:Variable.PType = "9508";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

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
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B Idle
        set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }
}

TestBasicIncoming95XXCallANALOG:
{
   // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B offhook
        set:User($UserB).cm_extn.DCP.HookChange = OffHook;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
        wait:$delay_time;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_ANALOG";set:Variable.PType = "9508";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "CALLING_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_ANALOG";set:Variable.PType = "9508";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
    }

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B Idle
        set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }
}

TestBasicOutgoingNortelCallANALOG:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B offhook
        set:User($UserB).cm_extn.DCP.HookChange = OffHook;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
        wait:$delay_time;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "CALLING_ANALOG";set:Variable.PType = "Nortel";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_ANALOG";set:Variable.PType = "Nortel";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

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
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B Idle
        set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }
}

TestBasicIncomingNortelCallANALOG:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "Nortel";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE
    set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B offhook
        set:User($UserB).cm_extn.DCP.HookChange = OffHook;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
        wait:$delay_time;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_ANALOG";set:Variable.PType = "Nortel";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "CALLING_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

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
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_ANALOG";set:Variable.PType = "Nortel";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B connected
        set:Variable.Usr = $UserB;set:Variable.State = "CALLING_CONN_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn1;
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
	  set:User($UserA).cm_extn.DCP.HookChange = OnHook;

    wait:$test_delay;

    // User A and User B idle
    sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
    }

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "9508";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    if($RunMode == Rig):
    {
        // User B Idle
        set:Variable.Usr = $UserB;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
        gosub:CheckDisplay;
        set:Variable.Btn = $OutgoingCallB_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
        gosub:CheckLamps;
    }
}


TestBasicOutgoingPOTSCallANALOG:
{
    // User A IDLE
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B IDLE (POTS) - no check

    if($RunMode == Rig):
    {
        // User B offhook
        set:User($UserB).cm_extn.FlashHook = True;
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSDialling;
        wait:$delay_time;

        // User B IDLE (POTS) - no check

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
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSOGConnReq;
    }

    // User A Ringing
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Flash";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Connected (POTS) - no check

    // User A Answers
    set:User($UserA).cm_extn.DCP.HookChange = OffHook;

    wait:$connect_time;

    // User A and User B connected
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.state=CMCSConnected;
    if($RunMode == Rig):
    {
        sync($sync_delay_time):User($UserB).cm_extn.current_ep.state=CMCSOGConnReq;
    }

    // Talkpath between A & B
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.GetActiveTone=CMLocalToneCutThru;
    sync($sync_delay_time):User($UserA).cm_extn.current_ep.media.localtone=CMLocalToneCutThru;

    // User A Connected
    set:Variable.Usr = $UserA;set:Variable.State = "CALLED_CONN_ANALOG";set:Variable.PType = "1516";set:Variable.OtherExtn=$IPOExtn2;
    //gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="On";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Connected (POTS) - no check

    // A & B onhook
  	set:User($UserA).cm_extn.DCP.HookChange = OnHook;
    if($RunMode == Rig):
    {
	      set:User($UserB).cm_extn.OnHook;
	      wait:1000;
        set:User($UserB).cm_extn.OnHook;
	      wait:1000;
        set:User($UserB).cm_extn.OnHook;
    }
    wait:$test_delay;

    // User A and User B idle
    //sync($sync_delay_time):User($UserA).cm_extn.state=CMCSIdle;
    //sync($sync_delay_time):User($UserB).cm_extn.state=CMCSIdle;
    //verify(Tone Verification Issue: $UserA is not idle):User($UserA).cm_extn.state=CMCSIdle;
    //verify(Tone Verification Issue: $UserB is not idle):User($UserB).cm_extn.state=CMCSIdle;

    // User A Idle
    set:Variable.Usr = $UserA;set:Variable.State = "IDLE";set:Variable.PType = "1516";set:Variable.OtherExtn="";
    gosub:CheckDisplay;
    set:Variable.Btn = $IncomingCallA_dssKey;set:Variable.GreenLp ="Off";set:Variable.RedLp ="On";
    gosub:CheckLamps;

    // User B Idle (POTS) - no check
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////

Configuration:
{
    report(*** Started doing phone configuration for test no: $TestID ***):<null>;

    if( $TestID == 1 ):
    {
        set:Variable.UserA = $x102_UserName;
        set:Variable.PhTyA = $x102_PhoneType;
        set:Variable.UserB = $x101_UserName;
        set:Variable.PhTyB = $x101_PhoneType;
        set:Variable.UserC = $x108_UserName;
        set:Variable.PhTyC = $x108_PhoneType;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.IncomingCallC_dssKey=0;
        set:Variable.OutgoingCall_dssKey=0;
        set:Variable.IPOExtn1 = 212; // IPOffice called number
        set:Variable.IPOExtn2 = 211; //IPOffice callback number
        set:Variable.TrunkID = 1; // Analog Trunk used to make incoming calls
    }
    if( $TestID == 2 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x102_UserName;
        set:Variable.UserC = $x108_UserName;
        set:Variable.VMCallA_dssKey = 0;
        set:Variable.VMCallB_dssKey = 0;
        set:Variable.VMCallC_dssKey = 0;
    }
    if( $TestID == 3 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.PhTyA = $x101_PhoneType;
        set:Variable.PartnerIP = 192.168.42.122;
    }
    // BRI
    if( $TestID == 4 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x102_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 555;
        set:Variable.IPOExtn2 = 102;
    }
    if( $TestID == 5 ):
    {
        set:Variable.UserA = $x102_UserName;
        set:Variable.UserB = $x101_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 555;
        set:Variable.IPOExtn2 = 101;
    }
    if( $TestID == 6 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x100_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 555;
        set:Variable.IPOExtn2 = 100;
    }
    if( $TestID == 7 ):
    {
        set:Variable.UserA = $x100_UserName;
        set:Variable.UserB = $x101_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 555;
        set:Variable.IPOExtn2 = 101;
    }
    if( $TestID == 8 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x108_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 555;
        set:Variable.IPOExtn2 = 108;
    }
    if( $TestID == 9 ):
    {
        set:Variable.UserA = $x108_UserName;
        set:Variable.UserB = $x101_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 555;
        set:Variable.IPOExtn2 = 101;
    }
    if( $TestID == 10 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x109_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 555;
        set:Variable.IPOExtn2 = 109;
    }
    if( $TestID == 11 ):
    {
        set:Variable.UserA = $x109_UserName;
        set:Variable.UserB = $x101_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 555;
        set:Variable.IPOExtn2 = 101;
    }
    if( $TestID == 12 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x106_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 555;
        set:Variable.IPOExtn2 = 106;
    }
    // SIP
    if( $TestID == 13 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x102_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 201;
        set:Variable.IPOExtn2 = 102;
        set:Variable.IPOExtn3 = 101;
    }
    if( $TestID == 14 ):
    {
        set:Variable.UserA = $x102_UserName;
        set:Variable.UserB = $x101_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 201;
        set:Variable.IPOExtn2 = 101;
        set:Variable.IPOExtn3 = 102;
    }
    if( $TestID == 15 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x100_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 201;
        set:Variable.IPOExtn2 = 100;
        set:Variable.IPOExtn3 = 101;
    }
    if( $TestID == 16 ):
    {
        set:Variable.UserA = $x100_UserName;
        set:Variable.UserB = $x101_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 201;
        set:Variable.IPOExtn2 = 101;
        set:Variable.IPOExtn3 = 100;
    }
    if( $TestID == 17 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x108_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 201;
        set:Variable.IPOExtn2 = 108;
        set:Variable.IPOExtn3 = 101;
    }
    if( $TestID == 18 ):
    {
        set:Variable.UserA = $x108_UserName;
        set:Variable.UserB = $x101_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 201;
        set:Variable.IPOExtn2 = 101;
        set:Variable.IPOExtn3 = 108;
    }
    if( $TestID == 19 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x109_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 201;
        set:Variable.IPOExtn2 = 109;
        set:Variable.IPOExtn3 = 101;
    }
    if( $TestID == 20 ):
    {
        set:Variable.UserA = $x109_UserName;
        set:Variable.UserB = $x101_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 201;
        set:Variable.IPOExtn2 = 101;
        set:Variable.IPOExtn3 = 109;
    }
    //POTS
    if( $TestID == 21 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x106_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 201;
        set:Variable.IPOExtn2 = 106;
        set:Variable.IPOExtn3 = 101;
    }
    // ANALOG
    if( $TestID == 22 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x102_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 212;
        set:Variable.IPOExtn2 = 211;
        set:Variable.TrunkID = 1; // Analog Trunk used to make incoming calls
    }
    if( $TestID == 23 ):
    {
        set:Variable.UserA = $x102_UserName;
        set:Variable.UserB = $x101_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 212;
        set:Variable.IPOExtn2 = 211;
        set:Variable.TrunkID = 1; // Analog Trunk used to make incoming calls
    }
    if( $TestID == 24 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x100_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 212;
        set:Variable.IPOExtn2 = 211;
        set:Variable.TrunkID = 1; // Analog Trunk used to make incoming calls
    }
    if( $TestID == 25 ):
    {
        set:Variable.UserA = $x100_UserName;
        set:Variable.UserB = $x101_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 212;
        set:Variable.IPOExtn2 = 211;
        set:Variable.TrunkID = 1; // Analog Trunk used to make incoming calls
    }
    if( $TestID == 26 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x108_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 212;
        set:Variable.IPOExtn2 = 211;
        set:Variable.TrunkID = 1; // Analog Trunk used to make incoming calls
    }
    if( $TestID == 27 ):
    {
        set:Variable.UserA = $x108_UserName;
        set:Variable.UserB = $x101_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 212;
        set:Variable.IPOExtn2 = 211;
        set:Variable.TrunkID = 1; // Analog Trunk used to make incoming calls
    }
    if( $TestID == 28 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x109_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 212;
        set:Variable.IPOExtn2 = 211;
        set:Variable.TrunkID = 1; // Analog Trunk used to make incoming calls
    }
    if( $TestID == 29 ):
    {
        set:Variable.UserA = $x109_UserName;
        set:Variable.UserB = $x101_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 212;
        set:Variable.IPOExtn2 = 211;
        set:Variable.TrunkID = 1; // Analog Trunk used to make incoming calls
    }
    //POTS
    if( $TestID == 30 ):
    {
        set:Variable.UserA = $x101_UserName;
        set:Variable.UserB = $x106_UserName;
        set:Variable.IncomingCallA_dssKey=0;
        set:Variable.OutgoingCallB_dssKey=0;
        set:Variable.IPOExtn1 = 212;
        set:Variable.IPOExtn2 = 211;
        set:Variable.TrunkID = 1; // Analog Trunk used to make incoming calls
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

    // IDLE
    if( $State == "IDLE" ):
    {
        report(** IDLE ***):<null>;
        if( $PType == "Nortel" ):
        {
            report(*** Nortel phone - do not check IDLE display ***):<null>;
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
        if( $PType == "9508" ):
        {
            report(*** 95xx phone - do not check IDLE display ***):<null>;
        }
    }
    // DIAL = user going offhook from IDLE state
    if( $State == "DIAL" ):
    {
        report(** DIAL ***):<null>;
        if( $PType == "Nortel" ):
        {
            // check only first line is empty
            set:Variable.line="Dial:           ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for DIAL screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line;
            set:Variable.line="Dir             ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for DIAL screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line;
        }
        if( $PType == "1508" ):
        {
            set:Variable.line="Dial: Number?           ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for DIAL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line;
            set:Variable.line="";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for DIAL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line;
            set:Variable.line="        Feature         ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for DIAL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line;
        }
        if( $PType == "1516" ):
        {
            set:Variable.line="Dial: Number?           ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for DIAL screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line;
            set:Variable.line="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for DIAL screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line;
            set:Variable.line="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for DIAL screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line;
            set:Variable.line="        Feature         ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for DIAL screen on line 3):User($Usr).cm_extn.DCP.Display[3]=$line;
        }
        if( $PType == "9508" ):
        {
            // check only title line
            set:Variable.line="Dial: Number?           ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for DIAL screen on line 1 ):User($Usr).cm_extn.DCP.Display[1]=$line;

        }
    }
    // RING - State associated to user ringing when it is being called from an internal extension
    if( $State == "RING" ):
    {
        report(** RING ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.line="$OtherExtn              ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for RING screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line;
            set:Variable.line="                        ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for RING screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$line;

        }
        if( $PType == "1508" ):
        {
            set:Variable.line="Call: Incoming          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RING screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line;
            set:Variable.line="o%$OtherExtn             ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RING screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line;
            set:Variable.line="         To VM   Ignore ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for RING screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line;
        }
        // not verified - to be rebuilt
        if( $PType == "1516" ):
        {
            set:Variable.line="Call: Incoming          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RING screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line;
            set:Variable.line="o%$OtherExtn             "
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RING screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line;
            set:Variable.line="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RING screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line;
            set:Variable.line="         To VM   Ignore ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for RING screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$line;
        }
    }
    //RINGBACK - State associated to user calling another internal extension
    if( $State == "RINGBACK" ):
    {
        report(** RINGBACK ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.line="$OtherExtn             ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for RINGBACK screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line;
        }
        // not verified - must be rebuilt
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
    }
    // Analog display
    // CALLING_ANALOG - State associated to user ringing when it is calling over Analog Trunk
    if( $State == "CALLING_ANALOG" ):
    {
        report(** CALLING_ANALOG ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.al="$OtherExtn      ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLING_ANALOG screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$al;
            set:Variable.al="                ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLING_ANALOG screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$al;

        }
        if( $PType == "1508" ):
        {
            set:Variable.al="Conn:            ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_ANALOG screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$al;
            set:Variable.al="v|a=External            ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_ANALOG screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$al;
            set:Variable.al="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_ANALOG screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$al;
        }
        if( $PType == "1516" ):
        {
            set:Variable.al="Conn:                ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_ANALOG screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$al;
            set:Variable.al="v|a=External            ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_ANALOG screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$al;
            set:Variable.al="$OtherExtn              ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_ANALOG screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$al;
            set:Variable.al="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_ANALOG screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$al;
        }
        if( $PType == "9508" ):
        {
            set:Variable.al="Connected: $OtherExtn   ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLING_ANALOG screen on line 1):User($Usr).cm_extn.DCP.Display[1]=$al;
            set:Variable.al="External                ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLING_ANALOG screen on line 2):User($Usr).cm_extn.DCP.Display[2]=$al;
        }
    }
    // CALLED_ANALOG - State associated to user ringing when it is being called from an external extension over Analog Trunk
    if( $State == "CALLED_ANALOG" ):
    {
        report(** CALLED_ANALOG ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.an="Extn$OtherExtn>75 ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLED_ANALOG screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$an;
            set:Variable.an="Info      Ignore";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLED_ANALOG screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$an;

        }
        if( $PType == "1508" ):
        {
            set:Variable.an="Call: Incoming          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_ANALOG screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$an;
            set:Variable.an="v%a=Extn$OtherExtn>75          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_ANALOG screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$an;
            set:Variable.an="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_ANALOG screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$an;
        }
        if( $PType == "1516" ):
        {
            set:Variable.an="Call: Incoming          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_ANALOG screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$an;
            set:Variable.an="v%a=Extn$OtherExtn>75          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_ANALOG screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$an;
            set:Variable.an="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_ANALOG screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$an;
            set:Variable.an="                 Ignore ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_ANALOG screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$an;
        }
        if( $PType == "9508" ):
        {
            set:Variable.an="Incoming: $OtherExtn     ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLED_ANALOG screen on line 1):User($Usr).cm_extn.DCP.Display[1]=$an;
            set:Variable.an="Extn$OtherExtn>75          ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLED_ANALOG screen on line 2):User($Usr).cm_extn.DCP.Display[2]=$an;
        }
    }
    // SIP display
    // CALLING_SIP - State associated to user ringing when it is calling over SIP Trunk
    if( $State == "CALLING_SIP" ):
    {
        report(** CALLING_SIP ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.sp="Extn$OtherExtn  ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLING_SIP screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sp;
            set:Variable.sp="$OtherExtn      ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLING_SIP screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$sp;

        }
        if( $PType == "1508" ):
        {
            set:Variable.sp="Call:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_SIP screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sp;
            set:Variable.sp="v|a=Extn$OtherExtn      ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_SIP screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sp;
            set:Variable.sp="$OtherExtn              ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_SIP screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sp;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sp="Call:                   ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_SIP screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sp;
            set:Variable.sp="v|a=Extn$OtherExtn      ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_SIP screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sp;
            set:Variable.sp="$OtherExtn              ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_SIP screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sp;
            set:Variable.sp="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_SIP screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sp;
        }
        if( $PType == "9508" ):
        {
            set:Variable.sp="Calling:";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLING_SIP screen on line 1):User($Usr).cm_extn.DCP.Display[1]=$sp;
            set:Variable.sp="Extn$OtherExtn         ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLING_SIP screen on line 2):User($Usr).cm_extn.DCP.Display[2]=$sp;
        }
    }
    // CALLED_SIP - State associated to user ringing when it is being called from an external extension over SIP Trunk
    if( $State == "CALLED_SIP" ):
    {
        report(** CALLED_SIP ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.sl="$OtherExtn>75   ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLED_SIP screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sl;
            set:Variable.sl="          Ignore";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLED_SIP screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$sl;

        }
        if( $PType == "1508" ):
        {
            set:Variable.sl="Call: Incoming          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_SIP screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sl;
            set:Variable.sl="v%a=$OtherExtn>75       ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_SIP screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sl;
            set:Variable.sl="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_SIP screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sl;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sl="Call: Incoming          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_SIP screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sl;
            set:Variable.sl="v%a=$OtherExtn>75       ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_SIP screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sl;
            set:Variable.sl="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_SIP screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sl;
            set:Variable.sl="                 Ignore ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_SIP screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sl;
        }
        if( $PType == "9508" ):
        {
            set:Variable.sl="Incoming: $OtherExtn     ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLED_SIP screen on line 1):User($Usr).cm_extn.DCP.Display[1]=$sl;
            set:Variable.sl="$OtherExtn>75          ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLED_SIP screen on line 2):User($Usr).cm_extn.DCP.Display[2]=$sl;
        }
    }
    // BRI display
    // CALLING_BRI - State associated to user ringing when it is calling over BRI Trunk
    if( $State == "CALLING_BRI" ):
    {
        report(** CALLING_BRI ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.bl="$OtherExtn      ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLING_BRI screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$bl;
            set:Variable.bl="                ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLING_BRI screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$bl;

        }
        if( $PType == "1508" ):
        {
            set:Variable.bl="Call:            ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_BRI screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$bl;
            set:Variable.bl="v|a=$OtherExtn     ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_BRI screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$bl;
            set:Variable.bl="                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_BRI screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$bl;
        }
        if( $PType == "1516" ):
        {
            set:Variable.bl="Call:            ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_BRI screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$bl;
            set:Variable.bl="v|a=$OtherExtn          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_BRI screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$bl;
            set:Variable.bl="                  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_BRI screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$bl;
            set:Variable.bl="                  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_BRI screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$bl;
        }
        if( $PType == "9508" ):
        {
            set:Variable.bl="Calling: ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLING_BRI screen on line 1):User($Usr).cm_extn.DCP.Display[1]=$bl;
            set:Variable.bl="$OtherExtn              ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLING_BRI screen on line 2):User($Usr).cm_extn.DCP.Display[2]=$bl;
        }
    }
    // CALLED_BRI - State associated to user ringing when it is being called from an external extension over BRI Trunk
    if( $State == "CALLED_BRI" ):
    {
        report(** CALLED_BRI ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.lm="$OtherExtn>75   ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLED_BRI screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$lm;
            set:Variable.lm="          Ignore";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLED_BRI screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$lm;

        }
        if( $PType == "1508" ):
        {
            set:Variable.lm="Call: Incoming          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_BRI screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$lm;
            set:Variable.lm="v%a=External>75         ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_BRI screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$lm;
            set:Variable.lm="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_BRI screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$lm;
        }
        if( $PType == "1516" ):
        {
            set:Variable.lm="Call: Incoming          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_BRI screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$lm;
            set:Variable.lm="v%a=External>75         ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_BRI screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$lm;
            set:Variable.lm="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_BRI screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$lm;
            set:Variable.lm="                 Ignore ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_BRI screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$lm;
        }
        if( $PType == "9508" ):
        {
            set:Variable.lm="Incoming: $OtherExtn";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLED_BRI screen on line 1):User($Usr).cm_extn.DCP.Display[1]=$lm;
            set:Variable.lm="External>75          ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLED_BRI screen on line 2):User($Usr).cm_extn.DCP.Display[2]=$lm;
        }
    }
    // Analog display
    // CALLING_CONN_ANALOG - State associated to user ringing when it is calling over Analog Trunk
    if( $State == "CALLING_CONN_ANALOG" ):
    {
        report(** CALLING_CONN_ANALOG ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.aj="$OtherExtn      ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLING_CONN_ANALOG screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$aj;
            set:Variable.aj="                ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLING_CONN_ANALOG screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$aj;

        }
        if( $PType == "1508" ):
        {
            set:Variable.aj="Conn:            ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_CONN_ANALOG screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$aj;
            set:Variable.aj="v|a=External            ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_CONN_ANALOG screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$aj;
            set:Variable.aj="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_CONN_ANALOG screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$aj;
        }
        if( $PType == "1516" ):
        {
            set:Variable.aj="Conn:                ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_CONN_ANALOG screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$aj;
            set:Variable.aj="v|a=External            ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_CONN_ANALOG screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$aj;
            set:Variable.aj="$OtherExtn              ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_CONN_ANALOG screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$aj;
            set:Variable.aj="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_CONN_ANALOG screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$aj;
        }
        if( $PType == "9508" ):
        {
            set:Variable.aj="Connected: $OtherExtn   ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLING_CONN_ANALOG screen on line 1):User($Usr).cm_extn.DCP.Display[1]=$aj;
            set:Variable.aj="External                ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLING_CONN_ANALOG screen on line 2):User($Usr).cm_extn.DCP.Display[2]=$aj;
        }
    }
    // CALLED_CONN_ANALOG - State associated to user ringing when it is being called from an external extension over Analog Trunk
    if( $State == "CALLED_CONN_ANALOG" ):
    {
        report(** CALLED_CONN_ANALOG ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.ak="Extn$OtherExtn   ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLED_CONN_ANALOG screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$ak;
            set:Variable.ak="$OtherExtn       ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLED_CONN_ANALOG screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$ak;

        }
        if( $PType == "1508" ):
        {
            set:Variable.ak="Conn:            ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_CONN_ANALOG screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$ak;
            set:Variable.ak="v|a=Extn$OtherExtn      ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_CONN_ANALOG screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$ak;
            set:Variable.ak="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_CONN_ANALOG screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$ak;
        }
        if( $PType == "1516" ):
        {
            set:Variable.ak="Conn:              ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_CONN_ANALOG screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$ak;
            set:Variable.ak="v|a=Extn$OtherExtn       ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_CONN_ANALOG screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$ak;
            set:Variable.ak="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_CONN_ANALOG screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$ak;
            set:Variable.ak="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_CONN_ANALOG screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$ak;
        }
        if( $PType == "9508" ):
        {
            set:Variable.ak="Connected: $OtherExtn     ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLED_CONN_ANALOG screen on line 1):User($Usr).cm_extn.DCP.Display[1]=$ak;
            set:Variable.ak="Extn$OtherExtn";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLED_CONN_ANALOG screen on line 2):User($Usr).cm_extn.DCP.Display[2]=$ak;
        }
    }
    // SIP display
    // CALLING_CONN_SIP - State associated to user ringing when it is calling over SIP Trunk
    if( $State == "CALLING_CONN_SIP" ):
    {
        report(** CALLING_CONN_SIP ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.si="$OtherExtn      ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLING_CONN_SIP screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$si;
            set:Variable.si="                ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLING_CONN_SIP screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$si;

        }
        if( $PType == "1508" ):
        {
            set:Variable.si="Conn:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_CONN_SIP screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$si;
            set:Variable.si="v|a=          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_CONN_SIP screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$si;
            set:Variable.si="$OtherExtn            ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_CONN_SIP screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$si;
        }
        if( $PType == "1516" ):
        {
            set:Variable.si="Conn:                   ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_CONN_SIP screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$si;
            set:Variable.si="v|a=                ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_CONN_SIP screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$si;
            set:Variable.si="$OtherExtn              ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_CONN_SIP screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$si;
            set:Variable.si="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_CONN_SIP screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$si;
        }
        if( $PType == "9508" ):
        {
            set:Variable.si="Connected: $OtherExtn";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLING_CONN_SIP screen on line 1):User($Usr).cm_extn.DCP.Display[1]=$si;
            set:Variable.si="                     ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLING_CONN_SIP screen on line 2):User($Usr).cm_extn.DCP.Display[2]=$si;
        }
    }
    // CALLED_CONN_SIP - State associated to user ringing when it is being called from an external extension over SIP Trunk
    if( $State == "CALLED_CONN_SIP" ):
    {
        report(** CALLED_CONN_SIP ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.sk="$OtherExtn      ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLED_CONN_SIP screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$sk;
            set:Variable.sk="                ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLED_CONN_SIP screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$sk;

        }
        if( $PType == "1508" ):
        {
            set:Variable.sk="Conn:             ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_CONN_SIP screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sk;
            set:Variable.sk="v|a=              ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_CONN_SIP screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sk;
            set:Variable.sk="$OtherExtn              ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_CONN_SIP screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sk;
        }
        if( $PType == "1516" ):
        {
            set:Variable.sk="Conn:               ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_CONN_SIP screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$sk;
            set:Variable.sk="v|a=                  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_CONN_SIP screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$sk;
            set:Variable.sk="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_CONN_SIP screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$sk;
            set:Variable.sk="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_CONN_SIP screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$sk;
        }
        if( $PType == "9508" ):
        {
            set:Variable.sk="Connected: $OtherExtn";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLED_CONN_SIP screen on line 1):User($Usr).cm_extn.DCP.Display[1]=$sk;
            set:Variable.sk="                     ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLED_CONN_SIP screen on line 2):User($Usr).cm_extn.DCP.Display[2]=$sk;
        }
    }
    // BRI display
    // CALLING_CONN_BRI - State associated to user ringing when it is calling over BRI Trunk
    if( $State == "CALLING_CONN_BRI" ):
    {
        report(** CALLING_CONN_BRI ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.bn="$OtherExtn      ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLING_CONN_BRI screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$bn;
            set:Variable.bn="                ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLING_CONN_BRI screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$bn;

        }
        if( $PType == "1508" ):
        {
            set:Variable.bn="Conn:            ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_CONN_BRI screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$bn;
            set:Variable.bn="v|a=External     ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_CONN_BRI screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$bn;
            set:Variable.bn="$OtherExtn        ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLING_CONN_BRI screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$bn;
        }
        if( $PType == "1516" ):
        {
            set:Variable.bn="Conn:            ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_CONN_BRI screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$bn;
            set:Variable.bn="v|a=External        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_CONN_BRI screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$bn;
            set:Variable.bn="$OtherExtn          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_CONN_BRI screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$bn;
            set:Variable.bn="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLING_CONN_BRI screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$bn;
        }
        if( $PType == "9508" ):
        {
            set:Variable.bn="Connected: $OtherExtn  ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLING_CONN_BRI screen on line 1):User($Usr).cm_extn.DCP.Display[1]=$bn;
            set:Variable.bn="External       ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLING_CONN_BRI screen on line 2):User($Usr).cm_extn.DCP.Display[2]=$bn;
        }
    }
    // CALLED_CONN_BRI - State associated to user ringing when it is being called from an external extension over BRI Trunk
    if( $State == "CALLED_CONN_BRI" ):
    {
        report(** CALLED_CONN_BRI ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.be="$OtherExtn      ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLED_CONN_BRI screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$be;
            set:Variable.be="                ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CALLED_CONN_BRI screen on line 2 ):User($Usr).cm_extn.DCP.Display[1]=$be;

        }
        if( $PType == "1508" ):
        {
            set:Variable.be="Conn:          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_CONN_BRI screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$be;
            set:Variable.be="v|a=External     ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_CONN_BRI screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$be;
            set:Variable.be="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CALLED_CONN_BRI screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$be;
        }
        if( $PType == "1516" ):
        {
            set:Variable.be="Conn:          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_CONN_BRI screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$be;
            set:Variable.be="v|a=External     ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_CONN_BRI screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$be;
            set:Variable.be="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_CONN_BRI screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$be;
            set:Variable.be="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CALLED_CONN_BRI screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$be;
        }
        if( $PType == "9508" ):
        {
            set:Variable.be="Connected: $OtherExtn  ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLED_CONN_BRI screen on line 1):User($Usr).cm_extn.DCP.Display[1]=$be;
            set:Variable.be="External             ";
            verify(Display Verification Issue: 9508 User: $Usr has incorrect info for CALLED_CONN_BRI screen on line 2):User($Usr).cm_extn.DCP.Display[2]=$be;
        }
    }
    //CONN - State associated to user connected to another internal extension
    if( $State == "CONN" ):
    {
        report(** CONN ***):<null>;
        if( $PType == "Nortel" ):
        {

            set:Variable.line="$OtherExtn                      ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CONN screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line;
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
    }
    //F590 - State associated to user dialling Feature 590
    if( $State == "F590" ):
    {
        report(** F590 ***):<null>;
        // not verified - to be rebuilt
        if( $PType == "Nortel" ):
        {
            set:Variable.xx="BE 8.1";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for F590 screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$xx;
        }
        // not verified - to be rebuilt
        if( $PType == "1508" ):
        {
            set:Variable.xx="Conn:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F590 screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$xx;
            set:Variable.xx="o|Extn$OtherExtn        ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F590 screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$xx;
            set:Variable.xx="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F590 screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$xx;
        }
        if( $PType == "1516" ):
        {
            set:Variable.xx="BE 8.1";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F590 screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$xx;
            set:Variable.xx="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F590 screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$xx;
            set:Variable.xx="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F590 screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$xx;
            set:Variable.xx="                  Exit  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F590 screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$xx;
        }
    }
    //F591 - State associated to user dialling Feature 591
    if( $State == "F591" ):
    {
        report(** F591 ***):<null>;
        // not verified - to be rebuilt
        if( $PType == "Nortel" ):
        {
            set:Variable.xv="$OtherExtn";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for F591 screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$xv;
        }
        // not verified - to be rebuilt
        if( $PType == "1508" ):
        {
            set:Variable.xv="$OtherExtn";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F591 screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$xv;
            set:Variable.xv="o|Extn$OtherExtn        ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F591 screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$xv;
            set:Variable.xv="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F591 screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$xv;
        }
        if( $PType == "1516" ):
        {
            set:Variable.xv="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F591 screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$xv;
            set:Variable.xv="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F591 screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$xv;
            set:Variable.xv="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F591 screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$xv;
            set:Variable.xv="                  Exit  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F591 screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$xv;
        }
    }
    //F592 - State associated to user dialling Feature 592
    if( $State == "F592" ):
    {
        report(** F592 ***):<null>;
        // not verified - to be rebuilt
        if( $PType == "Nortel" ):
        {
            set:Variable.xy="1324914493";
            if($RunMode == Simulator):
            {
                set:Variable.xy="No System SD";
            }
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for F592 screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$xy;
        }
        // not verified - to be rebuilt
        if( $PType == "1508" ):
        {
            set:Variable.xy="Conn:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F592 screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$xy;
            set:Variable.xy="o|Extn$OtherExtn        ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F592 screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$xy;
            set:Variable.xy="$OtherExtn                   >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for F592 screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$xy;
        }
        if( $PType == "1516" ):
        {
            set:Variable.xy="1324914493";
            if($RunMode == Simulator):
            {
                set:Variable.xy="No System SD";
            }
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F592 screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$xy;
            set:Variable.xy="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F592 screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$xy;
            set:Variable.xy="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F592 screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$xy;
            set:Variable.xy="                  Exit  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for F592 screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$xy;
        }
    }
    //VM_CONN - State associated to user connected to mailbox
    if( $State == "VM_CONN" ):
    {
        report(** VM_CONN ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.lk="Voicemail       ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for VM_CONN screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$lk;
        }
        if( $PType == "1508" ):
        {
            set:Variable.lk="Conn:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for VM_CONN screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$lk;
            set:Variable.lk="v|a=Voicemail           ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for VM_CONN screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$lk;
            set:Variable.lk="        Feature  Admin  ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for VM_CONN screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$lk;
        }
        if( $PType == "1516" ):
        {
            set:Variable.lk="Conn:                   ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for VM_CONN screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$lk;
            set:Variable.lk="v|a=Voicemail           ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for VM_CONN screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$lk;
            set:Variable.lk="                        ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for VM_CONN screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$lk;
            set:Variable.lk="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for VM_CONN screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$lk;
        }
    }
    //HOLD - State associated to user who puts on hold another internal user
    if( $State == "HOLD" ):
    {
        report(** HOLD ***):<null>;
        // not verified - to be rebuilt
        if( $PType == "Nortel" ):
        {
            set:Variable.line="";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for HOLD screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line;
        }
        if( $PType == "1508" ):
        {
            set:Variable.line1="Call: On-Hold           ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HOLD screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="o";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HOLD screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="$OtherExtn                    >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HOLD screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
        }
        if( $PType == "1516" ):
        {
            set:Variable.line1="Call: On-Hold           ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HOLD screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="v";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HOLD screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HOLD screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
            set:Variable.line4=" Pickup             ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HOLD screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$line4;
        }
    }
    //HELD - State associated to user who is put on hold by another internal user
    if( $State == "HELD" ):
    {
        report(** HELD ***):<null>;
        // not verified - to be rebuilt
        if( $PType == "Nortel" ):
        {
            set:Variable.line="";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for HELD screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line;
        }
        if( $PType == "1508" ):
        {
            set:Variable.line1="Held:                   ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HELD screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="o";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HELD screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="$OtherExtn                    >>";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for HELD screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
        }
        if( $PType == "1516" ):
        {
            set:Variable.line1="Held:                  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HELD screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line1;
            set:Variable.line2="v|                      ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HELD screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line2;
            set:Variable.line3="$OtherExtn";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HELD screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line3;
            set:Variable.line4="        Feature  Admin  ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for HELD screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$line4;
        }
    }
    //CONF - State associated to user being involved in a conference - CONF 100
    if( $State == "CONF" ):
    {
        report(** CONF ***):<null>;
        if( $PType == "Nortel" ):
        {
            set:Variable.line="Conf 100                ";
            verify(Display Verification Issue: Nortel User: $Usr has incorrect info for CONF screen on line 1 ):User($Usr).cm_extn.DCP.Display[0]=$line;

        }
        // not verified - to be rebuilt
        if( $PType == "1508" ):
        {
            set:Variable.line="Call: Incoming          ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CONF screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line;
            set:Variable.line="o%$OtherExtn             ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CONF screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line;
            set:Variable.line="         To VM   Ignore ";
            verify(Display Verification Issue: 1508 User: $Usr has incorrect info for CONF screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line;
        }
        // not verified - to be rebuilt
        if( $PType == "1516" ):
        {
            set:Variable.line="Call: Incoming          ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONF screen on line 1):User($Usr).cm_extn.DCP.Display[0]=$line;
            set:Variable.line="o%$OtherExtn             "
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONF screen on line 2):User($Usr).cm_extn.DCP.Display[1]=$line;
            set:Variable.line="";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONF screen on line 3):User($Usr).cm_extn.DCP.Display[2]=$line;
            set:Variable.line="         To VM   Ignore ";
            verify(Display Verification Issue: 1516 User: $Usr has incorrect info for CONF screen on line 4):User($Usr).cm_extn.DCP.Display[3]=$line;
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