/** @odoo-module **/

import { Component,useSubEnv,onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { getDefaultConfig } from "@web/views/view";
import { useService } from "@web/core/utils/hooks";
import { Domain } from "@web/core/domain";
import { Card } from "../../../../../awesome_tshirt/static/src/card/card";
import { PieChart } from "../piechart/piechart";
import {BarChart} from  "../bar/bar";
import { LineChart } from "../line/line";
import { NavCard } from "../navcard/navcard";

class EstateDashboard extends Component {
    
    setup() {
        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            },
        });

        this.action = useService("action");
        this.propertyService = useService("propertyService");

        this.keyToString = {
            total_properties: "Total Number of Properties",
            average_expected_price:"Average Expected Price",
            total_sold_properties:"Total Sold Properties",
            total_sales_revenue_last_7_days: "Total Sales Revenue (Last 7 Days)",
        };

        onWillStart(async () => {
            this.statistics = await this.propertyService.loadStatistics();
        });

        this.display = {
            controlPanel: { "top-right": false, "bottom-right": false },
        };
    }

    onProperty(){
        this.action.doAction("estate.estate_property_action");
        // const domain="[]"
        // this.Orders("Sold orders", domain);
    }

    Properties(title, domain) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: title,
            res_model: "estate.property",
            domain: new Domain(domain).toList(),
            views: [ 
                [false, "tree"],
                [false, "form"],
            ],
        });
    }

    openSoldProperties() {
        const domain = "[('state', '=', 'sold')]" 
        this.Properties("Sold orders", domain);
    }

    openUnsoldProperties(){
        const domain="[('state','!=','sold')]"
        this.Properties("Unsold orders", domain);

    }
    
    static template="estate.EstateDashboard";
}

EstateDashboard.components={Layout,NavCard,PieChart,BarChart,LineChart,Card}

registry.category("actions").add("estate.custom_dashboard", EstateDashboard);