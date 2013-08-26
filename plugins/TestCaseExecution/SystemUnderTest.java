/*
File: SystemUnderTest.java ; This file is part of Twister.
Version: 2.001

Copyright (C) 2012-2013 , Luxoft

Authors: Andrei Costachi <acostachi@luxoft.com>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
import javax.swing.JPanel;
import java.awt.Color;
import javax.swing.JSplitPane;
import java.awt.BorderLayout;
import javax.swing.SwingUtilities;
import java.awt.Dimension;

public class SystemUnderTest extends JPanel{
    public TestBeds tbs;
    public SUT sut;

    public SystemUnderTest(){
        tbs = new TestBeds();
        sut = new SUT();
        setLayout(new BorderLayout());
        final JSplitPane sp = new JSplitPane();
        sp.setLeftComponent(sut);
        sp.setRightComponent(tbs);
        sp.setOrientation(JSplitPane.HORIZONTAL_SPLIT);
        sp.setResizeWeight(0.5);
        SwingUtilities.invokeLater(new Runnable() {
                public void run() {
                    sp.setDividerLocation(0.5);
                }
            });
        add(sp,BorderLayout.CENTER);
    }
}