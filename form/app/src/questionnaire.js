import './questionnaire.css';
import './style/DatePicker.css';
import Select from 'react-select';
import DatePicker, { registerLocale } from 'react-datepicker';
import ru from 'date-fns/locale/ru';
import { useForm, Controller } from 'react-hook-form';
import axios from 'axios';
import regions from './utils/regions [MConverter.eu].js';
registerLocale('ru', ru);

function Questionnaire() {
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
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    control,
  } = useForm({
    mode: 'onChange',
    defaultValues: {
      region: 'Ваш регион',
      sex: 'Select...',
      has_children_below_18: 'Select...',
      family_status: 'Select...',
    },
  });

  function onSubmit(data) {
    let sendBody = {
      birthday_at: data.birthday_at,
      sex: data.sex,
      family_status: data.family_status.value,
      region: data.region.id,
      has_children_below_18:
        data.has_children_below_18 === 'Yes' ? true : false,
      tourism_goals: data.tourism_goals,
    };
    let sendEmail = data.email;

    console.log(JSON.stringify(sendBody));
    async function sendData() {
      try {
        await axios({
          method: 'POST',
          url: apiURL,
          params: {
            email: sendEmail,
          },
          headers: { 'Content-Type': 'application/json' },
          data: JSON.stringify(sendBody),
        });
      } catch (error) {
        console.log(error);
      }
    }

    const apiURL = 'https://api.recommender.suncake.xyz/questionnaire';

    sendData();
    reset();
  }

  return (
    <div className="form">
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="container">
          <h1>Анкета</h1>
          <div className=" box">
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
          <div className="">
            <Controller
              control={control}
              rules={{ required: true }}
              name="region"
              render={({ field: { onChange, value } }) => (
                <Select
                  onChange={onChange}
                  placeholder="Ваш регион"
                  noOptionsMessage={() => 'Регион не найден'}
                  options={listItem}
                  styles={colourStyles}
                ></Select>
              )}
            />
          </div>
          <div className="dateControl box">
            <label htmlFor="birthday_at">Дата рождения</label>
            <Controller
              control={control}
              rules={{ required: true }}
              name="birthday_at"
              render={({ field: { onChange, value } }) => (
                <DatePicker
                  dateFormat="dd/MM/yyyy"
                  placeholderText="ДД.ММ.ГГГГ"
                  onChange={onChange}
                  minDate={new Date('01/01/1900')}
                  maxDate={new Date()}
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
          <div className="sexChoose">
            <input
              {...register('sex', { required: true })}
              type="radio"
              value="male"
              id="male"
            />
            <label htmlFor="male"> Мужской</label>

            <input
              {...register('sex', { required: true })}
              type="radio"
              value="female"
              id="female"
            />
            <label htmlFor="female"> Женский</label>
          </div>
          <div className=" familyDiv ">
            <label htmlFor="family_status">Семейное положение</label>
            <Controller
              className="family_status"
              control={control}
              rules={{ required: true }}
              name="family_status"
              render={({ field: { onChange } }) => (
                <Select
                  onChange={onChange}
                  placeholder="Выберите..."
                  noOptionsMessage={() => 'Не найдено'}
                  options={[
                    { value: 'married', label: 'Женат/замужем' },
                    { value: 'in_relationship', label: 'Состою в отношениях' },
                    { value: 'single', label: 'Одинокий/одинокая' },
                  ]}
                  styles={colourStyles}
                ></Select>
              )}
            />
          </div>
          <div className=" familyDiv ">
            <label htmlFor="has_children_below_18">
              Несовершеннолетние дети
            </label>
            <Controller
              className="has_children_below_18"
              control={control}
              rules={{ required: true }}
              name="has_children_below_18"
              render={({ field: { onChange } }) => (
                <Select
                  onChange={onChange}
                  placeholder="Выберите..."
                  noOptionsMessage={() => 'Не найдено'}
                  options={[
                    { value: 'Yes', label: 'Да' },
                    { value: 'No', label: 'Нет' },
                  ]}
                  styles={colourStyles}
                ></Select>
              )}
            />
          </div>
          <div className="tourismCheck">
            <label> Вид туризма </label>
            <input
              type="checkbox"
              value="active"
              id="active"
              {...register('tourism_goals', { required: 'Выберите варианты' })}
            />{' '}
            <label htmlFor="active">Активный</label>
            <input
              type="checkbox"
              value="calm"
              id="calm"
              {...register('tourism_goals', { required: 'Выберите варианты' })}
            />{' '}
            <label htmlFor="calm">Спокойный</label>
            <input
              type="checkbox"
              value="cultural"
              id="cultural"
              {...register('tourism_goals', { required: 'Выберите варианты' })}
            />{' '}
            <label htmlFor="cultural">Культурный</label>
            <input
              type="checkbox"
              value="social"
              id="social"
              {...register('tourism_goals', { required: 'Выберите варианты' })}
            />{' '}
            <label htmlFor="social">Социальный</label>
            <div className="errMessage">
              {errors.tourism_goals && <p>{errors.tourism_goals.message}</p>}
            </div>
          </div>
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

export default Questionnaire;
