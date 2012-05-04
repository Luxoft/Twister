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
		Repository.frame.mainpanel.p4.dut.additem.setEnabled(true);
		Repository.frame.mainpanel.p4.dut.additem.setText("Add device");
		Repository.frame.mainpanel.p4.dut.remitem.setEnabled(true);
		Repository.frame.mainpanel.p4.dut.remitem.setText("Remove testbed");
		Repository.frame.mainpanel.p4.dut.temp0 = reference;
		Repository.frame.mainpanel.p4.dut.tname0.setText(name.toString());
		Repository.frame.mainpanel.p4.dut.tid0.setText(id.toString());
		Repository.frame.mainpanel.p4.dut.tdescription0.setText(description
				.toString());
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