if(window.EEA === undefined){
  var EEA = {
    who: 'eea.alchemy',
    version: '5.0'
  };
}

if(!EEA.AlchemyDiscoverer){
  EEA.AlchemyDiscoverer = {
    version: '5.0'
  };
}

EEA.AlchemyDiscoverer.Events = {
  contentTypesChanged: 'eea-alchemy-content-type-changed',
  lookInChanged: 'eea-alchemy-lookin-changed',
  lookForChanged: 'eea-alchemy-lookfor-changed',
  batchChanged: 'eea-alchemy-batch-changed',
  formSubmit: 'eea-alchemy-form-submit'
};

EEA.AlchemyDiscoverer.ContentTypesBox = function(context, options){
  var self = this;
  self.context = context;

  self.settings = {
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
}

EEA.AlchemyDiscoverer.ContentTypesBox.prototype = {
  initialize: function(){
    var self = this;

    self.context.fadeIn();

    // Handle events
    jQuery('input', self.context).click(function(evt){
      var options = {};
      options.checked = jQuery(this).parents('.alchemy-box').find(':checked');
      options.element = jQuery(this);
      jQuery(document).trigger(EEA.AlchemyDiscoverer.Events.contentTypesChanged, options);
    });

  }
};

EEA.AlchemyDiscoverer.LookInBox = function(context, options){
  var self = this;
  self.context = context;

  self.settings = {
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
}

EEA.AlchemyDiscoverer.LookInBox.prototype = {
  initialize: function(){
    var self = this;

    // Handle events
    jQuery('input', self.context).click(function(evt){
      var options = {};
      options.checked = jQuery(this).parents('.alchemy-box').find(':checked');
      options.element = jQuery(this);
      jQuery(document).trigger(EEA.AlchemyDiscoverer.Events.lookInChanged, options);
    });

    // Content-Type
    jQuery(document).bind(EEA.AlchemyDiscoverer.Events.contentTypesChanged, function(evt, options){
      if(!options.checked.length){
        self.context.find(':checked').attr('checked', false);
        jQuery(document).trigger(EEA.AlchemyDiscoverer.Events.lookInChanged, options);
        self.context.fadeOut();
      }else{
        self.context.fadeIn();
      }
    });
  }
};

EEA.AlchemyDiscoverer.LookForBox = function(context, options){
  var self = this;
  self.context = context;

  self.settings = {
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
}

EEA.AlchemyDiscoverer.LookForBox.prototype = {
  initialize: function(){
    var self = this;

    // Handle events
    jQuery('input', self.context).click(function(evt, item){
      var options = {};
      options.checked = jQuery(this).parents('.alchemy-box').find(':checked');
      options.element = jQuery(this);
      jQuery(document).trigger(EEA.AlchemyDiscoverer.Events.lookForChanged, options);
    });

    // Look in
    jQuery(document).bind(EEA.AlchemyDiscoverer.Events.lookInChanged, function(evt, options){
      if(!options.checked.length){
        self.context.find(':checked').attr('checked', false);
        jQuery(document).trigger(EEA.AlchemyDiscoverer.Events.lookForChanged, options);
        self.context.fadeOut();
      }else{
        self.context.fadeIn();
      }
    });
  }
};

EEA.AlchemyDiscoverer.BatchBox = function(context, options){
  var self = this;
  self.context = context;

  self.settings = {
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
}

EEA.AlchemyDiscoverer.BatchBox.prototype = {
  initialize: function(){
    var self = this;
    self.form = self.context.parents('form');
    self.select = self.context.find('select');

    // Handle events

    // Look for
    jQuery(document).bind(EEA.AlchemyDiscoverer.Events.lookForChanged, function(evt, options){
      if(!options.checked.length){
        self.context.fadeOut();
      }else{
        self.context.fadeIn();
      }
    });

    // Content-Type
    jQuery(document).bind(EEA.AlchemyDiscoverer.Events.contentTypesChanged, function(evt, options){
      if(options.checked.length){
        self.updateBatch();
      }
    });
  },

  // Validate search form
  updateBatch: function(){
    var self = this;

    var action = '@@alchemy.batch';
    var query = self.form.serialize();
    jQuery.get(action, query, function(data){
      self.select.empty();

      var batch = 0;
      var batch_size = '';
      data = parseInt(data, 10);
      while(batch < data){
        if(batch + 300 < data){
          batch_size = batch + '-' + (batch + 300);
        }else{
          batch_size = batch + '-' + data;
        }

        jQuery('<option>').val(batch_size).text(batch_size).appendTo(self.select);
        batch = batch + 300;
      }
    });
  }
};

EEA.AlchemyDiscoverer.ConsoleBox = function(context, options){
  var self = this;
  self.context = context;
  self.console = self.context.find('.alchemy-console');

  self.settings = {
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
}

EEA.AlchemyDiscoverer.ConsoleBox.prototype = {
  initialize: function(){
    var self = this;
    self.button = self.context.find('button');

    // Handle events
    self.button.click(function(){
      self.clear();
    });

    // Look for
    jQuery(document).bind(EEA.AlchemyDiscoverer.Events.lookForChanged, function(evt, options){
      if(!options.checked.length){
        self.context.fadeOut();
      }
    });

    // Form submit
    jQuery(document).bind(EEA.AlchemyDiscoverer.Events.formSubmit, function(evt, options){
      self.context.fadeIn();
      self.info(options.button.attr('value'));
      self.error(options.button.attr('value'));
      self.warning(options.button.attr('value'));
    });
  },

  info: function(msg){
    return this.log(msg, 'info');
  },

  error: function(msg){
    return this.log(msg, 'error');
  },

  warning: function(msg){
    return this.log(msg, 'warning');
  },

  log: function(msg, level){
    var self = this;
    level = level || 'info';
    var output = jQuery('<p>')
      .addClass(level)
      .text(msg +
        "Lorem Ipsum is simply dummy text of the " +
        "printing and typesetting industry. Lorem Ipsum " +
        "has been the industry's standard dummy text ever " +
        "since the 1500s, when an unknown printer took a galley " +
        "of type and scrambled it to make a type specimen book. " +
        "It has survived not only five centuries, but also the leap " +
        "into electronic typesetting, remaining essentially unchanged. " +
        "It was popularised in the 1960s with the release of Letraset " +
        "sheets containing Lorem Ipsum passages, and more recently with " +
        "desktop publishing software like Aldus PageMaker including versions " +
        "of Lorem Ipsum.")
      .appendTo(self.console);
    self.console.scrollTop(self.console[0].scrollHeight - self.console.height());
  },

  clear: function(){
    return this.console.empty();
  }
};


EEA.AlchemyDiscoverer.Form = function(context, options){
  var self = this;
  self.context = context;

  self.settings = {
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
};

EEA.AlchemyDiscoverer.Form.prototype = {
  initialize: function(){
    var self, boxes;

    self = this;
    self.form = self.context.find('form');
    self.buttons = jQuery('.alchemy-button', self.context);

    boxes = self.context.find('.alchemy-box')
    self.ctypes = new EEA.AlchemyDiscoverer.ContentTypesBox(jQuery(boxes[0]));
    self.lookin = new EEA.AlchemyDiscoverer.LookInBox(jQuery(boxes[1]));
    self.lookfor = new EEA.AlchemyDiscoverer.LookForBox(jQuery(boxes[2]));
    self.batch = new EEA.AlchemyDiscoverer.BatchBox(jQuery(boxes[3]));
    self.console = new EEA.AlchemyDiscoverer.ConsoleBox(jQuery(boxes[4]));

    // Events
    self.form.submit(function(evt){
      evt.preventDefault();
      return false;
    });

    self.buttons.find('input').click(function(evt){
      evt.preventDefault();
      var button = jQuery(this);
      return self.submit(button);
    });

    // Look For
    jQuery(document).bind(EEA.AlchemyDiscoverer.Events.lookForChanged, function(evt, options){
      if(!options.checked.length){
        self.buttons.fadeOut();
      }else{
        self.buttons.fadeIn();
      }
    });

    self.reload();
  },

  reload: function(){
    var self = this;
  },

  submit: function(button){
    var self = this;
    options = {};
    options.button = button;
    jQuery(document).trigger(EEA.AlchemyDiscoverer.Events.formSubmit, options);
  }
};

jQuery.fn.EEAlchemyDiscoverer = function(options){
  return this.each(function(){
    var context = jQuery(this);
    var adapter = new EEA.AlchemyDiscoverer.Form(context, options);
    context.data('EEAlchemyDiscoverer', adapter);
  });
};

// On document ready
jQuery(document).ready(function(){
  // Cleanup main template
  jQuery("#belowContent").remove();
  jQuery("#eea-comments").remove();
  jQuery(".discussion").remove();

  // Initialize
  jQuery('#eea-alchemy .alchemy-search').EEAlchemyDiscoverer();
});
