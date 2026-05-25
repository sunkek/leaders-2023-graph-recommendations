import './travel.css';
import './style/DatePicker.css';
import Select from 'react-select';
import CurrencyInput from 'react-currency-input-field';
import DatePicker, { registerLocale } from 'react-datepicker';
import ru from 'date-fns/locale/ru';
import { useForm, Controller } from 'react-hook-form';
import axios from 'axios';
import { useState } from 'react';
import regions from './utils/regions [MConverter.eu].js';
registerLocale('ru', ru);

function Travel() {
  const [isShown, setIsShown] = useState(false);
  const [state, setState] = useState({ lists: [] });

  function toggleSubmit() {
    setIsShown(!isShown);
  }
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const regArrays = Object.entries(regions);
  const listItem = regArrays.map((regArray) => {
    return {
      id: `${regArray[0]}`,

      label: `${regArray[1]}`,
    };
  });

  const colourStyles = {
    placeholder: (styles) => ({
      ...styles,
      color: '#a6a6a6',
      border: 'none',
    }),
    control: (styles) => ({
      ...styles,

      border: 0,
      boxShadow: 'none',
      width: '383px',
      height: '36px',
      paddingLeft: '9px',
      paddingRight: ' 9px',
    }),
    menuList: (styles) => ({
      ...styles,
      color: '#1D1D1D',
      maxHeight: '250px',

      '::-webkit-scrollbar': {
        width: '6px',
      },
      '::-webkit-scrollbar-track': {
        background: '#F5F5F5;',
      },
      '::-webkit-scrollbar-thumb': {
        background: '#FFCF08',
        borderRadius: '2px',
      },
      '::-webkit-scrollbar-thumb:hover': {
        background: '#555',
      },
    }),
    input: (styles) => ({
      ...styles,
      border: 'none',
    }),
    option: (styles, { isFocused, isSelected, isHover }) => ({
      ...styles,
      background: '#FFFFFF',
      color: isFocused ? '#A6A6A6' : isSelected ? '#1D1D1D' : undefined,
      zIndex: 1,
      '&:hover': {
        background: '#F5F5F5',
      },
    }),
    menu: (base) => ({
      ...base,
      zIndex: 100,
    }),
  };
  let year = new Date();

  let nextYear = year.setFullYear(year.getFullYear() + 1);
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    control,
  } = useForm({
    mode: 'onChange',
    defaultValues: {
      region: 'Куда едем?',
      budgetInput: '',
    },
  });
  function resetData(data) {
    reset();
  }
  function onSubmit(data) {
    const plus = new URLSearchParams();
    plus.append('object_type', 'restaurant');
    let sendBody = {
      email: data.email,
      region: data.region.id,
      date_start: data.date_start,
      date_end: data.date_end,
      budget: data.budgetInput,
      // object_type: 'restaurant',
    };

    async function sendData() {
      axios
        .get(apiURL, {
          params: sendBody,
        })

        .then((res) => {
          const lists = res.data;
          setState({ lists });
          console.log(state);
          toggleSubmit();
        })

        .catch(function (error) {
          console.log(error);
        })
        .finally(function () {});
    }

    const apiURL =
      'https://api.recommender.suncake.xyz/recommendation/user_based';

    sendData();
  }

  return (
    <div className="form">
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="container">
          <h1>Планирование поездки</h1>
          <div className="email">
            {' '}
            <label htmlFor="email">Ваш e-mail</label>
            <input
              className="textField"
              placeholder="name@mail.com"
              type="text"
              {...register('email', {
                required: 'Это обязательное поле',
                pattern: {
                  value:
                    /^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/,
                  message: 'Неверный формат',
                },
              })}
            ></input>
            <div className="errMessage">
              {errors?.email && <p>{errors?.email?.message}</p>}
            </div>
          </div>
          <div className="region">
            <Controller
              control={control}
              rules={{ required: true }}
              name="region"
              render={({ field: { onChange, value } }) => (
                <Select
                  onChange={onChange}
                  value={value}
                  placeholder="Куда едем?"
                  noOptionsMessage={() => 'Регион не найден'}
                  options={listItem}
                  styles={colourStyles}
                ></Select>
              )}
            />
          </div>
          <div className="dateControl">
            <label htmlFor="date_start">Дата поездки</label>
            <Controller
              control={control}
              rules={{ required: true }}
              name="date_start"
              render={({ field: { onChange, value } }) => (
                <DatePicker
                  dateFormat="dd/MM/yyyy"
                  placeholderText="ДД.ММ.ГГГГ"
                  onChange={(e) => {
                    setStartDate(e);
                    onChange(e);
                  }}
                  minDate={startDate}
                  maxDate={nextYear}
                  selectsStart
                  startDate={startDate}
                  endDate={endDate}
                  peekNextMonth
                  showMonthDropdown
                  showYearDropdown
                  dropdownMode="select"
                  locale="ru"
                  selected={value}
                />
              )}
            />
            <Controller
              control={control}
              rules={{ required: true }}
              name="date_end"
              render={({ field: { onChange, value } }) => (
                <DatePicker
                  dateFormat="dd/MM/yyyy"
                  placeholderText="ДД.ММ.ГГГГ"
                  onChange={onChange}
                  minDate={startDate}
                  maxDate={nextYear}
                  selectsEnd
                  startDate={startDate}
                  endDate={endDate}
                  peekNextMonth
                  showMonthDropdown
                  showYearDropdown
                  dropdownMode="select"
                  locale="ru"
                  selected={value}
                />
              )}
            />
          </div>
          <div className="budget">
            <label htmlFor="budgetInput">Введите бюджет на поездку</label>
            <Controller
              control={control}
              className="budgetInput"
              rules={{ required: true }}
              name="budgetInput"
              render={({ field: { onChange, value } }) => (
                <CurrencyInput
                  intlConfig={{ locale: 'ru' }}
                  id="input-example"
                  value={value}
                  className="textField"
                  suffix=" ₽"
                  placeholder="Введите сумму"
                  allowDecimals={false}
                  onValueChange={onChange}
                />
              )}
            />
          </div>
          {/* <ul>
            {state.lists.map((list) => (
              <li>{list}</li>
            ))}
          </ul> */}
          {isShown === true && (
            <div className="recomend">
              {state.lists.map((list) => {
                return (
                  <>
                    <p key={list}>{list} </p>
                  </>
                );
              })}
              <button className="resetButton" onClick={resetData}>
                {' '}
                Сбросить
              </button>
            </div>
          )}

          <div className="submitDiv">
            <button className="submitButton" type="submit">
              Отправить
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default Travel;
