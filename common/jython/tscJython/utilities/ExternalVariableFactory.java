
/**
*
* version: 1.000
*
* -*- coding: utf-8 -*-
*
* File: ExternalVariableFactory.java ; This file is part of Twister.
*
* Copyright (C) 2012 , Luxoft
*
* Authors:
*    Adrian Toader <adtoader@luxoft.com>
*
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at:
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*
*/


// Object Factory that is used to coerce python module into a Java class




package tscJython.utilities;

import tscJython.interfaces.ExternalVariableType;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.core.PyInteger;
import org.python.util.PythonInterpreter;

public class ExternalVariableFactory {

    private PyObject externalVariableClass;

    /**
     * Create a new PythonInterpreter object, to
     * execute some python code for importing
     * the python module that we will coerce.
     *
     * Once the module is imported than we obtain a reference to
     * it and assign the reference to a Java variable
     */

    public ExternalVariableFactory() {
        PythonInterpreter interpreter = new PythonInterpreter();

        interpreter.exec("import os, sys");
        interpreter.exec("sys.path.append(os.getcwd())");

        interpreter.exec("from jythonExternalVariableClass import ExternalVariable");
        externalVariableClass = interpreter.get("ExternalVariable");
    }

    /**
     * The create method is responsible for performing the actual
     * coercion of the referenced python module into Java bytecode
     */

    public ExternalVariableType create () {

        PyObject externalVariableObject = externalVariableClass.__call__();
        return (ExternalVariableType)externalVariableObject.__tojava__(ExternalVariableType.class);
    }

}
