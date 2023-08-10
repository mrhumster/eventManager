axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
moment.locale('ru');

const DATETIME_FORMAT = 'HH:mm DD.MM.YY (Z)'

const dt_format = ((value) => {
    if (value) {
        return moment(value).format(DATETIME_FORMAT)
    } else {
        return null
    }
})

const link_to_profile = ((username) => {
    return `/accounts/profile/${username}`
})

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
            const config = {
                headers:{
                    ETag: this.event.change_time,
              }
            };
            axios.get(`/api/events/${this.event.id}/`, config).then((response) => {
                this.event = response.data
            }).catch((error) => {
                if (error.response.status != 304) {
                    console.log(error)
                }
            })
        }
    },
    created() {
        this.get_event()
        setInterval(function () {
      		this.get_event();
    	}.bind(this), 2500);
    },
    template: `
<div class="card shadow mt-3" style="height: 95%">
  <div class="card-header bg-gradient bg-primary text-light  text-center">
    <h5 class="fw-light pt-1">Задачи на мероприятие: <a class="link-light link-offset-3" href="/${event.id}">[[ event.title ]]</a></h5>
  </div>
  <div class="card-body p-1 d-flex">
    <task-list></task-list>
    <task-browser :current_task="current_task" v-if="current_task" :key="current_task.id + current_task.executor + current_task.status"></task-browser>
  </div>
</div>
    `
})

app.component("task-control-panel", {
    compilerOptions: {
        delimiters: ['[[', ']]']
    },
    props: ['current_task'],
    template: `
<div class="d-grid gap-2 d-md-flex justify-content-md-end mt-5">
  <button class="btn btn-outline-success me-md-2 shadow"
          @click="setTaskStatus('PROGRESS')" 
          v-if="current_task.status == 'NEW'" 
          type="button"><i class="bi bi-play-circle pe-2"></i>Взять в работу
  </button>
  <button class="btn btn-outline-success me-md-2 shadow" 
          @click="setTaskStatus('CLOSED')" 
          v-if="current_task.status == 'PROGRESS'" type="button">
          <i class="bi bi-check-circle pe-2"></i>Завершить
  </button>
  <button class="btn btn-outline-success me-md-2 shadow" 
          @click="setTaskExecutor()"
          v-if="current_task.executor != ${user_id}" 
          type="button">
          <i class="bi bi-hand-thumbs-up pe-2"></i>Забрать себе [[ user_id ]]
  </button>
  <button class="btn btn-outline-success me-md-2 shadow" 
          @click="setTaskStatus('CANCEL')" 
          v-if="current_task.status != 'CANCEL'"  type="button">
          <i class="bi bi-trash pe-2"></i>Отменить
  </button>
  <button class="btn btn-outline-success me-md-2 shadow" 
          @click="setTaskStatus('NEW')" 
          v-if="current_task.status == 'CANCEL'"  type="button">
          <i class="bi bi-recycle pe-2"></i>Восстановить
  </button>
  
</div>
    `,
    methods: {
        async setTaskStatus(status) {
            await axios.patch(`/api/tasks/${this.current_task.id}/`, {status: status, executor: user_id})
                .then(response => {
                    this.$root.current_task = response.data
                })
                .catch(error => {
                    console.error('There was an error!', error);
                })
        },
        async setTaskExecutor() {
            await axios.patch(`/api/tasks/${this.current_task.id}/`, {executor: user_id})
                .then(response => {
                    this.$root.current_task = response.data
                })
                .catch(error => {
                    console.error('There was an error!', error);
                })
        }
    }
})

app.component('task-list', {
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    template: `
<div class="w-25" style="height: 99%;">
  <div class="border rounded-1" style="height: 100%;">
    <filter-status></filter-status>
    <!--<filter-executor v-if="this.$root.current_status_filter != 'NEW'"></filter-executor>-->
    <hr>
    <div class="d-flex flex-column align-item-stretch mt-2" style="height: 666px; overflow-y: auto; overflow-x: hidden">
      <task v-for="task in this.$root.event.tasks"
            :key="task.id"
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
<div class="d-grid gap-2 text-center pt-2 shadow border border-primary rounded-2 mt-3 py-1 mx-3">
  <div class="form-check form-switch ms-3">
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
    <div class="btn-group shadow mx-3" role="group" aria-label="Radio group filter by status">
      <input @click="onClickHandler($event)" type="radio" class="btn-check" name="btnradio" id="btnradio1" value="NEW" autocomplete="off" checked> 
      <label class="btn btn-outline-primary" for="btnradio1" title="Новые задачи"><i class="bi bi-asterisk"></i></label>
    
      <input @click="onClickHandler($event)" type="radio" class="btn-check" name="btnradio" id="btnradio2" VALUE="PROGRESS" autocomplete="off">
      <label class="btn btn-outline-primary" for="btnradio2" title="Задачи в работе"><i class="bi bi-hourglass-split"></i></label>
    
      <input @click="onClickHandler($event)" type="radio" class="btn-check" name="btnradio" id="btnradio3" value="CLOSED" autocomplete="off">
      <label class="btn btn-outline-primary" for="btnradio3" title="Завершенные задачи"><i class="bi bi-check2-square"></i></label>
      
      <input @click="onClickHandler($event)" type="radio" class="btn-check" name="btnradio" id="btnradio4" value="CANCEL" autocomplete="off">
      <label class="btn btn-outline-primary" for="btnradio4" title="Отмененные задачи"><i class="bi bi-trash"></i></label>
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
    data() {
        return {
            guest: null
        }
    },
    template: `
    <transition name="bounce">
    <button class="btn btn-outline-primary shadow mx-3 my-1" 
            @click="set_current_task" 
            v-if="task.status == statusFilter">
      <!--<small><span class="badge bg-primary">[[ task.status ]]</span></small><br>-->
      <span class="text-muted">[[ this.$root.task_descriptions[task.description] ]]</span><br> 
      <small><span v-if="this.guest">[[ this.guest.person.first_name ]] [[ this.guest.person.last_name ]]</span></small>
    </button>
    </transition>
    `,
    methods: {
        set_current_task() {
            this.$root.current_task = this.task
        },
        get_guest(guest_id) {
            axios.get(`/api/guests/${guest_id}`)
                .then((response) => {
                    this.guest = response.data
                })
                .catch(error => {
                    console.error(error)
                })
        }
    },
    mounted() {
        this.get_guest(this.task.guest)
    }
})

app.component('task-browser', {
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    props: ['current_task'],
    template: `
<div class="w-75 ps-1" style="height: 99%;">
  <div class="border rounded-1" style="height: 100%">
    <div class="d-flex flex-column align-items-center">
      <!--<h5 class="fw-light p-3">Задание [[ current_task.id ]]</h5>-->
        <div class="d-flex justify-content-between flex-wrap mt-5">
          <guest :guest_id="current_task.guest" :key="current_task.guest.id"></guest>
          <task-detail :task_id="current_task.id" :key="current_task.status"></task-detail>
        </div>
        <task-control-panel :current_task="current_task" v-if="current_task" :key="current_task.id"></task-control-panel>
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
            task: null,
            description: {
                // TODO: Вынести все эти описания на бэк
                'MERCH': 'Выдать раздаточный материал'
            }
        }
    },
    created() {
        this.get_task(this.task_id)
    },
    methods: {
        get_task(task_id) {
            axios.get(`/api/tasks/${task_id}/`).then((response) => {
                this.task = response.data
                this.task.created_time = dt_format(this.task.created_time)
                this.task.progress_time = dt_format(this.task.progress_time)
                this.task.closed_time = dt_format(this.task.closed_time)
                this.task.cancel_time = dt_format(this.task.cancel_time)
            }).catch((error) => {
                console.log(error)
            })
        }
    },
    template: `
<div class="card shadow ms-3" v-if="task" style="width: 24rem;">
  <div class="card-header text-center">
    <p class="card-title fw-light pt-2"><task-status :status="task.status"></task-status></p>
  </div>
  <div class="card-body d-flex flex-column">
    <h5 class="card-text fw-light text-center flex-grow-1">[[ description[task.description] ]]</h5>
    <div class="row" v-if="task.created_time">
      <div class="col-5 text-end text-muted">Создана</div>
      <div class="col-7">[[ task.created_time ]]</div>
    </div>
    <div class="row" v-if="task.progress_time">
      <div class="col-5 text-end text-muted">В работу</div>
      <div class="col-7">[[ task.progress_time ]]</div>
    </div>
    <div class="row" v-if="task.closed_time">
      <div class="col-5 text-end text-muted">Закрыта</div>
      <div class="col-7">[[ task.closed_time ]]</div>
    </div>
    <div class="row" v-if="task.cancel_time">
      <div class="col-5 text-end text-muted">Отменена</div>
      <div class="col-7">[[ task.cancel_time ]]</div>
    </div>
    
  </div>
  <div class="card-footer text-end" style="min-height: 3rem">
    <task-executor v-if="task.executor" :guest_id="task.executor" :key="task.executor"></task-executor>
  </div>
</div>
    `
})

app.component('task-executor', {
    compilerOptions: {
        delimiters: ['[[', ']]']
    },
    props: ['guest_id'],
    created() {
        if (this.guest_id != null) {
            this.get_person(this.guest_id)
        }
    },
    data() {
        return {
            guest: null
        }
    },
    methods: {
        get_person(guest_id) {
            axios.get(`/api/guests/${guest_id}/`).then((response) => {
                this.guest = response.data
                this.guest.registered_time = dt_format(this.guest.registered_time)
                this.guest.visited_time = dt_format(this.guest.visited_time)
                this.guest.cancel_time = dt_format(this.guest.cancel_time)
                this.guest.link_to_profile = link_to_profile(this.guest.person.username)
            }).catch((error) => {
                console.log(error)
            })
        }
    },
    template: `
    <div v-if="guest"><i class="bi bi-person-circle pe-2"></i>
      <a class="link-primary link-offset-3" :href="guest.link_to_profile">[[ guest.person.first_name ]] [[ guest.person.last_name ]]</a>
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
<div class="card shadow" v-if="guest" style="width: 24rem;">
  <img v-if="guest.image" :src="guest.image" class="card-img-top" alt="...">
  <div class="card-body" v-if="guest">
    <h5 class="card-text">[[ guest.person.first_name ]] [[ guest.person.last_name ]]</h5>
    <!--<a class="link-primary" href="mailto:[[guest.person.email]]">[[ guest.person.email ]]</a>-->
    <div class="row" v-if="guest.registered_time">
      <div class="col-5 text-end text-muted">Зарегистрирован</div>
      <div class="col-7">[[ guest.registered_time ]]</div>
    </div>
    <div class="row" v-if="guest.visited_time">
      <div class="col-5 text-end text-muted">Пришел</div>
      <div class="col-7">[[ guest.visited_time ]]</div>
    </div>
    <div class="row" v-if="guest.refused_time">
      <div class="col-5 text-end text-muted">Отказался</div>
      <div class="col-7">[[ guest.refused_time ]]</div>
    </div>
  </div>
</div>
    `,
    created() {
        this.get_person(this.guest_id)
    },
    methods: {
        get_person(guest_id) {
            axios.get(`/api/guests/${guest_id}/`).then((response) => {
                this.guest = response.data
                this.guest.registered_time = dt_format(this.guest.registered_time)
                this.guest.visited_time = dt_format(this.guest.visited_time)
                this.guest.cancel_time = dt_format(this.guest.cancel_time)
                this.guest.refused_time = dt_format(this.guest.refused_time)
            }).catch((error) => {
                console.log(error)
            })
        }
    }
})

app.component('task-status', {
    props: ['status'],
    template: `
<span v-if="status == 'NEW'"><i class="bi bi-asterisk pe-2"></i>Новая задача</span>
<span v-if="status == 'PROGRESS'"><i class="bi bi-hourglass-split pe-2"></i>В работе</span>
<span v-if="status == 'CLOSED'"><i class="bi bi-check2-square pe-2"></i>Закрыта</span>
<span v-if="status == 'CANCEL'"><i class="bi bi-trash pe-2"></i></i>Отменена</span>
    `
})

app.mount('#app')