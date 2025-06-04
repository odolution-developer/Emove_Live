
/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import LineComponent from "@stock_barcode/components/line";
import MainComponent from "@stock_barcode/components/main";
import PackageLineComponent from "@stock_barcode/components/package_line";

import { onMounted } from "@odoo/owl";

patch(LineComponent.prototype, {

    setup() {
        super.setup?.(); // ensure the base setup is called if it exists

        onMounted(() => {
            console.log(this.props);
        });
    },
});

// patch(PackageLineComponent.prototype, {

//     setup() {
//         super.setup?.(); // ensure the base setup is called if it exists

//         onMounted(() => {
//             console.log(this.props);
//         });
//     },
// });
// patch(MainComponent.prototype, {

//     setup() {
//         super.setup?.(); // ensure the base setup is called if it exists

//         onMounted(() => {
//             console.log(this.props);
//         });
//     },
// });
