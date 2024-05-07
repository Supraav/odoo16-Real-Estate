/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class EmptyDashboard extends Component {
    static template = "client_actions.EmptyDashboard";
    
}

registry.category("actions").add("client_actions.dashboard_menu", EmptyDashboard);