/*
File: TestMySftp.java ; This file is part of Twister.
Version: 2.003
Copyright (C) 2012 , Luxoft

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
package com.twister;

import javax.swing.JFrame;
import javax.swing.JTextField;

public class TestMySftp {
	
	public static void main(String [] args){
		JFrame f = new JFrame();
		JTextField field = new JTextField();
		field.setText("/home/tscguest//twister/config/email.xml");
		f.add(field);
		f.setVisible(true);
		MySftpBrowser sftpbrows = new MySftpBrowser("tsc-server", "tscguest", "tscguest","8000", field, f,false);
		f.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
	}
}
