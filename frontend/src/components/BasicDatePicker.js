import { Calendar } from 'react-date-range';

class MyComponent extends Component {
  handleSelect(date){
    console.log(date); // native Date object
  }



}<Calendar
        date={new Date()}
        onChange={this.handleSelect}
      />