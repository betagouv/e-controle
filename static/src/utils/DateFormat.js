import moment from 'moment'
import 'moment/locale/fr';

export default function (value) {
    moment.locale('fr');
    if (value) {
        return moment(String(value)).format('D MMMM YYYY');
    }
}
