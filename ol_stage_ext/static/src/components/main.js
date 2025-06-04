/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import MainComponent from "@stock_barcode/components/main";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart } from "@odoo/owl";

import { onMounted } from "@odoo/owl";

patch(MainComponent.prototype, {
    
    setup() {
        super.setup();
        this.notification = useService("notification");
        // state={...this.state,selected_line:0}
        // console.log(state)
        onMounted(() => {
            console.log(this.props);
        });
    },
    
    get lines() {
        const sortedLines = [...this.env.model.groupedLines].sort((a, b) => {
            const codeA = a.product_id?.code?.toUpperCase() || "";
            const codeB = b.product_id?.code?.toUpperCase() || "";
            return codeA.localeCompare(codeB);
        });
        console.log("sorted lines by code", sortedLines);
        return sortedLines;
    },
    
    
    async validiateandgeneratecoupon(ev) {
        let selectedLine = document.querySelector('.o_sublines .o_barcode_line.o_highlight');
        const isSubline = Boolean(selectedLine);
        if (!selectedLine) {
            selectedLine = document.querySelector('.o_barcode_line.o_highlight');}
            const SelectedLine_id= selectedLine?selectedLine.dataset.virtualId:0
            console.log(SelectedLine_id,this.state)
        // this.onBarcodeScanned('8470000375255')
        console.log(this.env.model)
        console.log("before selected line id",selectedLine.dataset.virtual)
        if (SelectedLine_id){
            
            const selected_line=this.lines.filter((line)=>{
                console.log("line_data",line)
                console.log("line_id",line.id,SelectedLine_id,line.id === parseInt(SelectedLine_id))
                return line.virtual_id === parseInt(SelectedLine_id)
                
            })
            // console.log("selected_line",SelectedLine_id,selected_line,this.lines)
            if (!selected_line.length>0){
                console.log('selected line')
                return
            }
            console.log("after selected line")
            console.log("selected",selected_line.qty_done,selected_line.quantity,selected_line)
            const result = await this.rpc('/generate_coupon', {
                line_id:selected_line[0].id,
                qty_done:selected_line[0].qty_done,
                quantity:selected_line[0].quantity,
                move_id:selected_line[0].move_id,
                sorted_lines:this.env.model.groupedLines
                // qty_done:selected_line.qty_done,
                // quantity:selected_line.quantity,
                
            });
            console.log("after selected line 2")
            // this.notification.add(result.status, {type: "danger"});
            console.log(result)
            
            if (Array.isArray(result)) {
                result.forEach((res) => {
                    const msg = res.coupon_code ? `${res.status}: ${res.coupon_code}` : res.status;
                    this.notification.add(msg, { type: "info" });
                });
            } 
            else {
                this.notification.add(result.status || "Unexpected response", { type: "warning" });
            }
            
            // Validate the batch
            // await this.env.model.validate();
            
            // Go to Main Screen 
            // await this.env.services.action.doAction('stock_barcode_picking_batch.stock_barcode_batch_picking_action_kanban');
            // console.log(this.env.services.action.doAction('stock_barcode_picking_batch.stock_barcode_batch_picking_action_kanban'));
            
            
            
        }
    },
    // get lines() {
        //     console.log("line",this.env.model.groupedLines)
        //     return this.env.model.groupedLines;
        // },
        
        // get firstPickingState() {
            //     return line.product_id?.state;
            // },
            
            
    get pickingStates() {
        const states = this.lines.reduce((acc, line) => {
        const state = line.picking_id?.state;
            if (state && !acc.includes(state)) {
                acc.push(state);
            }
            return acc;
        }, []);

        console.log(states);
        return states;
    },


    get clusters() {
    let _clusters = this.lines.reduce((acc, line) => {
        let packages = line.product_id?.packages || {};
        const packageNames = Object.keys(packages);
        packageNames.forEach((packageName) => {
            if (!acc[packageName])
                acc[packageName]=packages[packageName]
        });
        return acc;
    }, {});
    _clusters = Object.keys(_clusters).map((cluster)=>{
        return {
            name:cluster,
            color:_clusters[cluster]
        }
    })

    console.log(_clusters);
    return _clusters
    }

})