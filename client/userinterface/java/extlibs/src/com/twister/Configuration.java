/*
File: Configuration.java ; This file is part of Twister.
Version: 3.001
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

//configuration class used in Item to represent configurations
public class Configuration{
	private boolean enabled = true;
	private boolean ieratorOD,iteratorSOF;//OD-onlyDefault,SOF-stoponfail
	private String file;
	
	public Configuration(String file){
		this.file = file;
	}

	public boolean isEnabled() {
		return enabled;
	}

	public void setEnabled(boolean enabled) {
		this.enabled = enabled;
	}

	public boolean isIeratorOD() {
		return ieratorOD;
	}

	public void setIeratorOD(boolean ieratorOD) {
		this.ieratorOD = ieratorOD;
	}

	public boolean isIteratorSOF() {
		return iteratorSOF;
	}

	public void setIteratorSOF(boolean iteratorSOF) {
		this.iteratorSOF = iteratorSOF;
	}

	public String getFile() {
		return file;
	}

	public void setFile(String file) {
		this.file = file;
	}
}