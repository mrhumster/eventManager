axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
moment.locale('ru');

const app = Vue.createApp({
    data() {
        return {
            user_id: null,
            event: {},
            tasks: null,
            current_task: null,
            current_status_filter: 'NEW',
            only_my_tasks: false,
            task_descriptions: {
                'MERCH': 'Выдать мерч'
            }
        }
    },
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    methods: {
        get_event() {
            this.event['id'] = event.id
            axios.get(`/${this.event.id}/api/event/`).then((response) => {
                this.event = response.data
            }).catch((error) => {
                console.log(error)
            })
        },
        get_tasks() {
            axios.get(`/${this.event.id}/api/tasks/`).then((response) => {
                this.tasks = response.data
            }).catch((error) => {
                console.log(error)
            })
        }
    },
    created() {
        this.get_event()
        this.get_tasks()
    },
    template: `
<div class="card shadow mt-3" style="height: 90vh">
  <div class="card-header">
    <h5 class="fw-light p-1">[[ event.title ]]</h5>
  </div>
  <div class="card-body p-1 d-flex">
    <task-list></task-list>
    <task-browser :current_task="current_task" v-if="current_task" :key="current_task.id"></task-browser>
  </div>    
</div>
    `
})

app.component('task-list', {
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    template: `
<div class="w-25">
  <div class="border rounded-1" style="height: 100%">
    <filter-status></filter-status>
    <filter-executor v-if="this.$root.current_status_filter != 'NEW'"></filter-executor>
    <hr>
    <div class="d-flex flex-column mt-2">
      <task v-for="task in this.$root.tasks" 
            :task="task" 
            :statusFilter="this.$root.current_status_filter"
            :executorFilter="this.$root.current_executor_filter">      
      </task>
    </div>
  </div>
</div>
    `
})

app.component('filter-executor', {
    template: `
<div class="d-grid gap-2 text-center pt-2">
  <div class="form-check form-switch ms-5">
    <input v-model="this.$root.only_my_tasks" class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault">
    <label class="form-check-label" for="flexSwitchCheckDefault">Только мои задачи</label>
  </div>
</div>
    `
})

app.component('filter-status', {
    template: `
<div class="d-grid gap-2 text-center pt-3">
    <!--<div class="fw-light pt-1">Фильтр задач по статусу</div> -->
    <div class="btn-group mx-3" role="group" aria-label="Radio group filter by status">
      <input @click="onClickHandler($event)" type="radio" class="btn-check" name="btnradio" id="btnradio1" value="NEW" autocomplete="off" checked> 
      <label class="btn btn-outline-primary" for="btnradio1" title="Новые задачи"><i class="bi bi-person-up"></i></label>
    
      <input @click="onClickHandler($event)" type="radio" class="btn-check" name="btnradio" id="btnradio2" VALUE="PROGRESS" autocomplete="off">
      <label class="btn btn-outline-primary" for="btnradio2" title="Задачи в работе"><i class="bi bi-person-lock"></i></label>
    
      <input @click="onClickHandler($event)" type="radio" class="btn-check" name="btnradio" id="btnradio3" value="CLOSED" autocomplete="off">
      <label class="btn btn-outline-primary" for="btnradio3" title="Завершенные задачи"><i class="bi bi-person-check"></i></label>
      
      <input @click="onClickHandler($event)" type="radio" class="btn-check" name="btnradio" id="btnradio4" value="CANCEL" autocomplete="off">
      <label class="btn btn-outline-primary" for="btnradio4" title="Отмененные задачи"><i class="bi bi-person-slash"></i></label>
    </div>
</div>
    `,
    methods: {
        onClickHandler(e) {
            this.$root.current_status_filter = e.currentTarget.value
            if (e.currentTarget.value === 'NEW') {
                this.$root.only_my_tasks = false
            }
        }
    }
})

app.component('task', {
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    props: ['task', 'statusFilter', 'executorFilter'],
    template: `
    <button class="btn btn-outline-primary mx-3 my-1" 
            @click="set_current_task" 
            v-if="task.status == statusFilter">
      <span class="badge bg-primary">[[ task.status ]]</span> [[ this.$root.task_descriptions[task.description] ]]
    </button>
    `,
    methods: {
        set_current_task() {
            console.log('click')
            this.$root.current_task = this.task
        }
    }
})

app.component('task-browser', {
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    props: ['current_task'],
    template: `
<div class="w-75 ps-1">
  <div class="border rounded-1" style="height: 100%">
    <div class="d-flex flex-column align-items-center">
       <h5 class="fw-light p-3">Задание [[ current_task.id ]]</h5>
       <div class="d-flex">
        <guest :guest_id="current_task.guest" :key="current_task.guest.id"></guest>
        <task-detail :task_id="current_task.id" :key="current_task.id"></task-detail>
       </div>
    </div>
  </div>
</div>
    `
})

app.component('task-detail', {
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    props: ['task_id'],
    data() {
        return {
            task: null
        }
    },
    created() {
        this.get_task(this.task_id)
        console.log(moment())
    },
    methods: {
        get_task(id) {
            axios.get(`/${id}/api/task/`).then((response) => {
                this.task = response.data
            }).catch((error) => {
                console.log(error)
            })
        }
    },
    template: `
<div class="card shadow ms-3" style="width: 24rem;">
  [[ task ]]
</div>
    `
})

app.component('guest', {
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    props: ['guest_id'],
    data() {
        return {
            guest: null
        };
    },
    template: `
<div class="card shadow" style="width: 24rem;">
  <img src="/static/img/guest.png" class="card-img-top" alt="...">
  <div class="card-body" v-if="guest">
    <h5 class="card-text">[[ guest.person.first_name ]] [[ guest.person.last_name ]]</h5>
    <a class="link-primary" href="mailto:[[guest.person.email]]">[[ guest.person.email ]]</a>
    <div class="row" v-if="guest.registered_time">
      <div class="col-5 text-end text-muted">Зарегистрирован</div>
      <div class="col-7">[[ guest.registered_time.format('HH:mm DD.MM.YY (Z)') ]]</div>
    </div>
    <div class="row" v-if="guest.visited_time">
      <div class="col-5 text-end text-muted">Пришел</div>
      <div class="col-7">[[ guest.visited_time.format('HH:mm DD.MM.YY (Z)') ]]</div>
    </div>
    <div class="row" v-if="guest.refused_time">
      <div class="col-5 text-end text-muted">Отказался</div>
      <div class="col-7">[[ guest.refused_time.format('HH:mm DD.MM.YY (Z)') ]]</div>
    </div>
  </div>
</div>
    `,
    created() {
        this.get_person(this.guest_id)
        console.log(moment())
    },
    methods: {
        get_person(id) {
            axios.get(`/${id}/api/guest/`).then((response) => {
                this.guest = response.data
                this.guest.registered_time = moment(response.data.registered_time)
                this.guest.visited_time = moment(response.data.visited_time)
                this.guest.cancel_time = moment(response.data.cancel_time)
            }).catch((error) => {
                console.log(error)
            })
        }
    }
})


app.mount('#app')