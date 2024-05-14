/** @odoo-module **/

import { Component,useSubEnv } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { getDefaultConfig } from "@web/views/view";
import { useService } from "@web/core/utils/hooks";
import { Domain } from "@web/core/domain";
import { PieChart } from "../chart/piechart";
 

class CustomDashboard extends Component {
    static template = "project_dashboard.CustomDashboard";

    setup() {
        this.action = useService("action");
        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            },
        });
    }

    onCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    onOrders(){
        console.log("hello");
    }

    openOrders(title, domain) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: title,
            res_model: "awesome_tshirt.order",
            domain: new Domain(domain).toList(),
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    static components={Layout,PieChart}
}

registry.category("actions").add("project_dashboard.dashboard_menu", CustomDashboard);