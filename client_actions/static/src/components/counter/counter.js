/** @odoo-module **/

import { Component,useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import {Extract} from "../extract/extract"
import {Todo} from "../todo/todo"
import { TodoList } from "../todo_list/todo_list";
 
class Counter extends Component {
    static template = "client_actions.Counter";
    setup() {
        this.state = useState({ value: 0 });
    }
    increment() {
        this.state.value++;
    }
    decrement(){
        this.state.value--;
    }
    
    static components = {Extract,TodoList}
}

registry.category("actions").add("client_actions.counter_menu", Counter);