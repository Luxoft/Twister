/*
File: TestBed.java ; This file is part of Twister.

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
import javax.swing.JPanel;
import java.awt.Color;
import java.awt.event.MouseMotionAdapter;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.Point;
import javax.swing.JLabel;
import javax.swing.BorderFactory;
import javax.swing.border.BevelBorder;
import java.util.ArrayList;
import javax.swing.JTextField;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.Dimension;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.DefaultMutableTreeNode;

public class TestBed {

	private int X, Y;
	String name = "";
	String description = "";
	String id = "";
	ArrayList<Device> devices = new ArrayList<Device>();
	TestBed reference;

	public TestBed() {
		reference = this;
	}

	public void updateInfo() {
		Repository.window.mainpanel.p4.getDut().additem.setEnabled(true);
		Repository.window.mainpanel.p4.getDut().additem.setText("Add device");
		Repository.window.mainpanel.p4.getDut().remitem.setEnabled(true);
		Repository.window.mainpanel.p4.getDut().remitem
				.setText("Remove testbed");
		Repository.window.mainpanel.p4.getDut().temp0 = reference;
		Repository.window.mainpanel.p4.getDut().tname0.setText(name.toString());
		Repository.window.mainpanel.p4.getDut().tid0.setText(id.toString());
		Repository.window.mainpanel.p4.getDut().tdescription0
				.setText(description.toString());
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public void setID(String id) {
		this.id = id;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String toString() {
		return "TestBed: " + name.toString();
	}

	public void addDevice(Device device) {
		devices.add(device);
	}
}
